import pandas as pd
import os
import math

# ==========================================
# 0. 核心配置
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 假设数据文件都放在脚本同级目录下的 'Sumerian_Shang_King_Match' 文件夹中
DATA_DIR = os.path.join(BASE_DIR, 'Sumerian_Shang_King_Match')

FILE_MAP = {
    'S1': os.path.join(DATA_DIR, 'SKL_Xie_score.csv'),
    'S2': os.path.join(DATA_DIR, 'SKL Xie score Hai.csv'),
    'S3': os.path.join(DATA_DIR, 'SKL Xie score Heng.csv'),
    'S4': os.path.join(DATA_DIR, 'SKL Xie score Shang Jia.csv'),
    'S5': os.path.join(DATA_DIR, 'SKL Xie score Bao Yi.csv')
}
def get_m(val):
    if val >= 1.0: return 100.0
    if val >= 0.5: return 10.0
    return 0.01

def get_tight_multiplier(dist): return 1.5 if dist <= 2 else (1.0 if dist <= 5 else 0.01)

# ==========================================
# 1. 加载数据库
# ==========================================
dbs = {f'S{i}': {} for i in range(1, 6)}
for role, filename in FILE_MAP.items():
    try:
        # 0:ID, 1:Name, 3:NS, 6:TS, 8:Time(第九列), 9:DS
        df = pd.read_csv(filename, header=0, encoding='utf-8-sig').iloc[:, [0, 1, 3, 6, 8, 9]]
        df.columns = ['ID', 'Name', 'NS', 'TS', 'Time', 'DS']
        for _, row in df.iterrows():
            try:
                kid = int(float(row['ID']))
                dbs[role][kid] = {
                    'name': str(row['Name']).strip(),
                    'time': str(row['Time']).strip(),
                    'n': float(row['NS']), 't': float(row['TS']), 'd': float(row['DS'])
                }
            except: continue
    except Exception as e:
        print(f"❌ 加载 {role} 失败: {e}")

# ==========================================
# 2. 计算前十名战队
# ==========================================
all_paths = []
s4_list = []
for kid, k in dbs['S4'].items():
    actual_t = k['t'] if kid >= 122 else (0.5 if k['t'] >= 0.5 else 0.01)
    s4_list.append({'id': kid, 'm': get_m(k['n']) * get_m(actual_t) * get_m(k['d'])})

for s4_node in s4_list:
    s4_id = s4_node['id']
    for s5_id in range(s4_id + 1, s4_id + 6):
        if s5_id not in dbs['S5']: continue
        pair_m = s4_node['m'] * get_m(dbs['S5'][s5_id]['n']) * get_m(dbs['S5'][s5_id]['t']) * get_m(dbs['S5'][s5_id]['d']) * get_tight_multiplier(s5_id - s4_id)
        
        for s3_id in range(s4_id - 5, s4_id):
            if s3_id not in dbs['S3']: continue
            for s2_id in range(max(1, s3_id - 100), s3_id):
                if s2_id not in dbs['S2']: continue
                for s1_id in range(max(1, s2_id - 100), s2_id):
                    if s1_id not in dbs['S1']: continue
                    
                    m_anc = (get_m(dbs['S1'][s1_id]['n']) * 100 * get_m(dbs['S1'][s1_id]['d'])) * \
                            (get_m(dbs['S2'][s2_id]['n']) * 100 * get_m(dbs['S2'][s2_id]['d'])) * \
                            (get_m(dbs['S3'][s3_id]['n']) * 100 * get_m(dbs['S3'][s3_id]['d']))
                    
                    idx = math.log10(max(m_anc * pair_m, 1e-25))
                    all_paths.append({'ids': [s1_id, s2_id, s3_id, s4_id, s5_id], 'idx': idx})

all_paths.sort(key=lambda x: x['idx'], reverse=True)
top_10 = all_paths[:10]

# ==========================================
# 3. 构造 CSV 数据并导出
# ==========================================
csv_rows = []
for i, t in enumerate(top_10, 1):
    row = {'排名': i, '真龙指数': round(t['idx'], 2)}
    for j, kid in enumerate(t['ids']):
        step = f"S{j+1}"
        k_data = dbs[step][kid]
        row[f'{step}_ID'] = kid
        row[f'{step}_名字'] = k_data['name']
        row[f'{step}_统治时间'] = k_data['time']
        row[f'{step}_城市(手动填)'] = "" # 预留空白列
    csv_rows.append(row)

# 导出文件
output_file = 'Top_10_True_Dragon_Final.csv'
pd.DataFrame(csv_rows).to_csv(output_file, index=False, encoding='utf-8-sig')

print(f"\n✅ 处理完成！前十名战报已导出至: {output_file}")
print("📊 你可以直接用 Excel 打开该文件，在 '城市(手动填)' 列中补入相关信息。")
