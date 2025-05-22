import ezdxf
import matplotlib.pyplot as plt
import os
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from matplotlib import font_manager
from PIL import Image


#  フォルダパスを指定
folder_path = "C:/Users/yasud/Documents/src2"
dxf_files = ["test_file1_answer.dxf"]

# 日本語フォント（明瞭やIPAexGothicがなければ別の日本語フォントに変えてください）
# WindowsのMeiryoフォントを直接指定する例
font_path = "C:/Windows/Fonts/meiryo.ttc"
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# 変換処理
for dxf_file in dxf_files:
    dxf_path = os.path.join(folder_path, dxf_file)
    png_path = os.path.join(folder_path, dxf_file.replace(".dxf", ".png"))

    # DXFファイル読み込み
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()

    # 描画準備
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_axes([0, 0, 1, 1])

    # 高精度描画コンテキスト
    ctx = RenderContext(doc)
    ctx.set_current_layout(msp)
    backend = MatplotlibBackend(ax)
    
                
    # 描画実行
    Frontend(ctx, backend).draw_layout(msp)
    
     
    # 画像の反転
    fig.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"✅ {png_path} を保存しました。")

    # 色反転処理（PNG保存後に実行）
    img = Image.open(png_path).convert("RGB")
    pixels = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            # 青はそのまま
            if b > 150 and r < 100 and g < 100:
                continue
            # 白 → 黒、黒 → 白
            elif r > 200 and g > 200 and b > 200:
                pixels[x, y] = (0, 0, 0)
            elif r < 50 and g < 50 and b < 50:
                pixels[x, y] = (255, 255, 255)

    # 保存（名前変更して保存）
    inverted_path = png_path.replace(".png", "_inverted.png")
    img.save(inverted_path)
    print(f"✅ 色反転画像を保存しました：{inverted_path}")

    # 画像の反転


    # 保存
    fig.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.close(fig)


print("🎉 すべてのDXFファイルを高精度でPNGへ変換しました。")
