import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('data/capacity.csv', names=['rain', 'cloth'])
df['cloth_adj'] = df['cloth'][df['cloth'] < 400]

cnt_list = []
width = 20
for i in range(len(df['cloth_adj'])):
    if(i%width == 0):
        cnt = 0
        cloth_10 = df['cloth_adj'][i: i+width]
        for j in cloth_10:
            if j<200:
                cnt += 1
        cnt_list.append(cnt)
    
# グラフの設定
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(cnt_list, marker='o', markersize=4, linewidth=1.5, color='blue', label='count of capacity < 200')
ax.axhline(y=8, color='red', linestyle='--', linewidth=1, label='Threshold(8 times)')

ax.set_xlabel(f'Window Number ({width} samples each)', fontsize=13)
ax.set_ylabel(f'Count of Capacity < 200', fontsize=13)
ax.set_ylim(-0.5, width + 0.5)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('data/capacity.png', dpi=300, bbox_inches='tight')
plt.show()