import ezdxf
import matplotlib.pyplot as plt
import os

# フォルダパス（DXFファイルが保存されているフォルダの場所を自身のの環境に合わせて変更）
folder_path = "C:/Users/yasud/Documents/src2"

# 日本語フォント（環境に合わせて調整）
plt.rcParams['font.family'] = 'Meiryo' 

# 対象のDXFファイル
dxf_files = ["test_file1_answer.dxf"]

def clean_text(text):
    # 文字化け対策：表示できない文字を除去
    try:
        # 文字コードが壊れている部分を除去して置き換え
        clean = text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        return clean    
    except:
        return "[文字化け]"

# メイン処理
for dxf_file in dxf_files:
    # パスと対象のDXFファイルを結合
    file_path = os.path.join(folder_path, dxf_file)
    # DXFファイルを読み込む
    doc = ezdxf.readfile(file_path)
    # モデルスペースを取得
    msp = doc.modelspace()
    # 図全体（fig）と、描画領域（ax）を作る
    fig, ax = plt.subplots()

# モデルスペースの中にある全ての図形（線や文字など）を一つずつ取り出す
    for e in msp:
        if e.dxftype() == 'LINE':
            start, end = e.dxf.start, e.dxf.end
            # 線を書く
            ax.plot([start[0], end[0]], [start[1], end[1]], color='black')

        elif e.dxftype() == 'CIRCLE':
            center, radius = e.dxf.center, e.dxf.radius
            circle = plt.Circle((center[0], center[1]), radius, fill=False, color='green')
            # 円や弧を書く
            ax.add_patch(circle)

        elif e.dxftype() == 'ARC':
            from matplotlib.patches import Arc
            center = e.dxf.center
            radius = e.dxf.radius
            start_angle = e.dxf.start_angle
            end_angle = e.dxf.end_angle
            arc = Arc((center[0], center[1]), 2*radius, 2*radius,
                    angle=0, theta1=start_angle, theta2=end_angle, color='black')
            # 円や弧を書く
            ax.add_patch(arc)

        elif e.dxftype() == 'TEXT':
            raw_text = e.dxf.text
            text = clean_text(raw_text)
            pos = e.dxf.insert
            # 文字を書く
            ax.text(pos[0], pos[1], text, fontsize=10, color='blue')

        elif e.dxftype() == 'MTEXT':
            raw_text = e.text
            text = clean_text(raw_text)
            pos = e.dxf.insert
            # 文字を書く
            ax.text(pos[0], pos[1], text, fontsize=10, color='blue')

        elif e.dxftype() == 'LWPOLYLINE':
            points = [(p[0], p[1]) for p in e.get_points()]
            x, y = zip(*points)
            # 線を書く
            ax.plot(x, y, color='purple')

        elif e.dxftype() == 'INSERT':
            # ブロック挿入（簡易的に十字で描画）
            pos = e.dxf.insert
            # 線を書く
            ax.plot([pos[0]-5, pos[0]+5], [pos[1], pos[1]], color='red')
            ax.plot([pos[0], pos[0]], [pos[1]-5, pos[1]+5], color='red')

        elif e.dxftype() == 'DIMENSION':
            # 寸法線（寸法値のテキストだけ表示）
            try:
                text = clean_text(e.dxf.text)
                pos = e.dxf.defpoint
                ax.text(pos[0], pos[1], f"⟷ {text}", fontsize=8, color='brown')
            except:
                pass

    # 縦横の比率を1：1に保つ
    ax.axis('equal')
    # 目盛りや枠線を非表示にする
    ax.axis('off')

    output_file = dxf_file.replace(".dxf", ".png")
    output_path = os.path.join(folder_path, output_file)
    plt.savefig(output_path, dpi=3000, bbox_inches='tight')
    plt.close()
    
    print(f"{output_file} を保存しました。")

print("✅ 全てのファイルを変換しました。")
