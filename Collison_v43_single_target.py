import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import thin
from scipy.spatial.distance import cdist
import os

def get_nodes(skel):
    """提取骨架节点：端点和交叉点"""
    kernel = np.array([[1, 1, 1], [1, 10, 1], [1, 1, 1]], dtype=np.uint8)
    filtered = cv2.filter2D(skel.astype(np.uint8), -1, kernel)
    return np.argwhere((filtered == 11) | (filtered >= 13))

def get_v43_features(binary_img, size=256, prune_iters=7):
    """
    v43 极限平滑版：
    1. 中值滤波（3x3）消除笔画边缘锯齿
    2. 7层深度剪枝，只留主干
    """
    coords = np.argwhere(binary_img > 0)
    if len(coords) == 0: return None, None, None
    y0, x0 = coords.min(axis=0); y1, x1 = coords.max(axis=0)
    h_orig, w_orig = y1 - y0 + 1, x1 - x0 + 1
    cropped = binary_img[y0:y1+1, x0:x1+1]
    
    # 比例对齐与填充
    if h_orig / w_orig > 5.0 or w_orig / h_orig > 5.0:
        scale = size / max(h_orig, w_orig)
        new_h, new_w = int(h_orig * scale), int(w_orig * scale)
        resized = cv2.resize(cropped, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        final_img = np.zeros((size, size), dtype=np.uint8)
        dy, dx = (size - new_h) // 2, (size - new_w) // 2
        final_img[dy:dy+new_h, dx:dx+new_w] = resized
    else:
        final_img = cv2.resize(cropped, (size, size), interpolation=cv2.INTER_LINEAR)

    # --- 核心平滑升级 ---
    # 1. 中值滤波去噪
    final_img = cv2.medianBlur(final_img, 3)
    # 2. 闭运算填补缝隙
    kernel_smooth = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    final_img = cv2.morphologyEx(final_img, cv2.MORPH_CLOSE, kernel_smooth)
    
    # 骨架化
    skel = thin(final_img > 0).astype(np.uint8)
    
    # 3. 深度剪枝（7次），彻底干掉毛刺
    for _ in range(prune_iters):
        kernel = np.array([[1, 1, 1], [1, 10, 1], [1, 1, 1]], dtype=np.uint8)
        f = cv2.filter2D(skel, -1, kernel)
        skel[f == 11] = 0
        skel = thin(skel > 0).astype(np.uint8)

    pts = np.argwhere(skel > 0)
    nodes = get_nodes(skel)
    return pts, nodes, skel

def get_grid_direction_v43(skel, grid_size=5):
    """5x5 格阵方向，提高统治力判断的纯净度"""
    h, w = skel.shape
    gh, gw = h // grid_size, w // grid_size
    grid_feats = []
    
    grad_x = cv2.Sobel(skel.astype(float), cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(skel.astype(float), cv2.CV_64F, 0, 1, ksize=3)
    
    for i in range(grid_size):
        for j in range(grid_size):
            roi_x = grad_x[i*gh:(i+1)*gh, j*gw:(j+1)*gw]
            roi_y = grad_y[i*gh:(i+1)*gh, j*gw:(j+1)*gw]
            energy_x = np.sum(np.abs(roi_x))
            energy_y = np.sum(np.abs(roi_y))
            total = energy_x + energy_y + 1e-6
            
            # 保持 0.6 阈值，但在更平滑的线上，这个值会更稳定
            if energy_x / total > 0.6: grid_feats.append(1)
            elif energy_y / total > 0.6: grid_feats.append(2)
            else: grid_feats.append(0) 
    return np.array(grid_feats)

def apply_proportional_spine_v49(skel_o, penalty_factor=0.05):
    h, w = skel_o.shape
    # 扩大检测范围到中间 30%
    side_margin = int(w * 0.35) 
    center_zone = skel_o[:, side_margin : w - side_margin]
    
    # 计算全图骨架像素总数
    total_pixels = np.sum(skel_o > 0)
    # 计算中轴带内的像素总数
    center_pixels = np.sum(center_zone > 0)
    
    if total_pixels == 0: return 1.0
    
    # 核心比例：文字的骨头应该大部分长在脊梁上
    spine_ratio = center_pixels / total_pixels
    
    # 酒瓶子的骨头都在两边的“耳朵”和“肚子”上，比例会很低
    # 商字的骨头集中在中间，比例会很高
    if spine_ratio < 0.4: # 如果中间的骨头不到全身的 40%
        return 1.0 - penalty_factor
    return 1.0
    
    # 逻辑：必须上半或下半有『极度居中』的笔画
    if not has_top and not has_bottom:
        return 1.0 - penalty_factor
    return 1.0

def run_v43_logic(p_sumer, obi_dir):
    SIZE = 256
    img_s = cv2.imread(p_sumer, cv2.IMREAD_GRAYSCALE)
    bin_s = (img_s < 127).astype(np.uint8) if np.mean(img_s) > 127 else (img_s > 127).astype(np.uint8)
    # 苏美尔：依然保持轻微平滑
    pts_s, nodes_s, skel_s = get_v43_features(bin_s, SIZE, prune_iters=1)
    feat_grid_s = get_grid_direction_v43(skel_s)

    results = []
    for f in os.listdir(obi_dir):
        if not f.lower().endswith('.png'): continue
        img_o = cv2.imread(os.path.join(obi_dir, f), cv2.IMREAD_GRAYSCALE)
        bin_o = (img_o < 127).astype(np.uint8) if np.mean(img_o) > 127 else (img_o > 127).astype(np.uint8)
        # OBI/Jinwen：深度平滑（7次剪枝）
        pts_o, nodes_o, skel_o = get_v43_features(bin_o, SIZE, prune_iters=7)
        
        if pts_o is not None:
            # 1. Cover (50%)
            d_back = cdist(pts_s, pts_o, metric='euclidean')
            cover_score = (np.sum(np.min(d_back, axis=1) < 15) / len(pts_s)) * 100
            # 2. Topology (20%)
            if len(nodes_o) > 0 and len(nodes_s) > 0:
                d_topo = cdist(nodes_o, nodes_s, metric='euclidean')
                topo_score = np.exp(-(np.mean(np.min(d_topo, axis=1))**2) / (2 * 25.0**2)) * 100
            else: topo_score = 0
            # 3. Grid Direction (30%)
            feat_grid_o = get_grid_direction_v43(skel_o)
            valid_idx = np.where(feat_grid_s > 0)[0]
            grid_score = (np.sum(feat_grid_s[valid_idx] == feat_grid_o[valid_idx]) / len(valid_idx)) * 100 if len(valid_idx) > 0 else 0
            
            final_raw = (cover_score * 0.5 + topo_score * 0.2 + grid_score * 0.3)
            # 2. 调用脊梁惩罚函数 (Backbone Check)
            # feat_grid_s 是苏美尔的 5x5 向量, feat_grid_o 是目标的
            penalty = apply_proportional_spine_v49(skel_o)

            # 3. 最终得分 = 原始分 * 惩罚系数
            final_adjusted = final_raw * penalty

            # 4. 存入结果 (增加一个 Penalty 项方便观察)
            results.append({
                'name': f, 
                'final': final_adjusted, 
                'penalty': penalty, # 1.0 表示满分，0.6 表示被重砍了
                'cover': cover_score, 
                'topo': topo_score, 
                'grid': grid_score,
                'skel': skel_o,
                'nodes': nodes_o
                })
            
    results.sort(key=lambda x: x['final'], reverse=True)

    print(f"\n📡 v43.0 [极限平滑模式] Pruning: 7 | MedianBlur: On")
    print(f"{'Rank':<4} | {'Filename':<35} | {'Final%':<8} | {'Cover%':<8} | {'Topo%':<8} | {'Grid%':<8}| {'penalty':<8}")
    print("-" * 90)
    for i, r in enumerate(results[:10], 1):
        print(f"{i:<4} | {r['name']:<35} | {r['final']:>7.1f}% | {r['cover']:>7.1f}% | {r['topo']:>7.1f}% | {r['grid']:>7.1f}%| {r['penalty']:>7.1f}")
    # 可视化 (代码同 v41，保持黄色节点)
    # ...
    
# 绘图逻辑 (2行6列，第一行Base+Rank1-5，第二行留白+Rank6-10完美对齐)
    top_n = min(10, len(results))
    
    # 画布大小：2行6列，保证文字和细节都能看清
    fig, axes = plt.subplots(2, 6, figsize=(30, 10))
    
    # 1. 第一行最左侧 (Row 0, Col 0): BASE 目标图
    axes[0, 0].set_title("BASE: Sumerian\n(Yellow Nodes)", fontsize=14)
    axes[0, 0].imshow(skel_s, cmap='gray')
    if len(nodes_s) > 0:
        axes[0, 0].scatter(nodes_s[:, 1], nodes_s[:, 0], c='yellow', s=25)
    axes[0, 0].axis('off')

    # 2. 第二行最左侧 (Row 1, Col 0): 刻意留白，支撑对齐结构
    axes[1, 0].axis('off')

    # 3. 循环放置 Top 10 的结果图
    for i in range(top_n):
        res = results[i]
        ov = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
        
        # 背景：苏美尔（深灰色） / 前景：匹配目标（青色）
        ov[skel_s > 0] = [60, 60, 60]
        ov[res['skel'] > 0] = [0, 255, 255]
        
        # 核心排版算法：自动计算行和列
        # i < 5 时在第 0 行，i >= 5 时在第 1 行
        row = 0 if i < 5 else 1
        # 列索引始终从 1 开始（因为 0 号位给了 Base 和 留白）
        col = (i % 5) + 1 
        
        axes[row, col].set_title(f"Rank {i+1}\n{res['name']}\nScore: {res['final']:.1f}%", fontsize=12)
        axes[row, col].imshow(ov)
        if len(res['nodes']) > 0:
            axes[row, col].scatter(res['nodes'][:, 1], res['nodes'][:, 0], c='yellow', s=18)
        axes[row, col].axis('off')

    # 4. 安全机制：如果识别结果不足 10 个，关掉多余的空白坐标轴
    for i in range(top_n, 10):
        row = 0 if i < 5 else 1
        col = (i % 5) + 1
        axes[row, col].axis('off')

    plt.tight_layout()
    plt.show()
  #  turn off visuallization

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR_SUMERIAN = os.path.join(BASE_DIR, "sample_data_sumerian")
DATA_DIR_OBI = os.path.join(BASE_DIR, "sample_data_obi")


if __name__ == "__main__":
    # 动态拼接文件名，彻底取代 D 盘绝对路径
    sumerian_target = os.path.join(DATA_DIR_SUMERIAN, "Sumerian_shang.png")
    
    # 传入相对路径变量
    run_v43_logic(sumerian_target, DATA_DIR_OBI)
