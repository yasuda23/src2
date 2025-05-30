import os
import ezdxf
import matplotlib.pyplot as plt
import japanize_matplotlib
import matplotlib.font_manager as fm
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from PIL import Image

# フォルダパスを指定（適宜変更）
folder_path = "C:/Users/yasud/Documents/src2"
dxf_files = ["test_file1_answer.dxf", "test_file2_answer.dxf"]

for dxf_file in dxf_files:
    dxf_path = os.path.join(folder_path, dxf_file)
    png_path = os.path.join(folder_path, dxf_file.replace(".dxf", ".png"))

    try:
        if not os.path.isfile(dxf_path):
            print(f" {dxf_file} が見つかりません")
            continue

        try:
            doc = ezdxf.readfile(dxf_path, encoding="cp932")
        except Exception as e:
            print(f" 読み込み失敗: {dxf_file} → {e}")
            continue

        #  すべての文字スタイルに対してMSゴシックを適用
        for style in doc.styles:
            style.dxf.font = "msgothic.ttc"

        msp = doc.modelspace()

        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_axes([0, 0, 1, 1])

        ctx = RenderContext(doc)
        ctx.set_current_layout(msp)
        backend = MatplotlibBackend(ax)
        Frontend(ctx, backend).draw_layout(msp)

        fig.savefig(png_path, dpi=300, bbox_inches='tight')
        plt.close(fig)

        # 色反転処理
        img = Image.open(png_path).convert("RGB")
        pixels = img.load()
        width, height = img.size
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                if b > 150 and r < 100 and g < 100:
                    continue
                elif r > 200 and g > 200 and b > 200:
                    pixels[x, y] = (0, 0, 0)
                elif r < 50 and g < 50 and b < 50:
                    pixels[x, y] = (255, 255, 255)

        img.save(png_path)
        print(f" PNG変換完了: {dxf_file}")

    except Exception as e:
        print(f" エラー発生: {dxf_file} → {e}")
