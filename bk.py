import ezdxf
import matplotlib.pyplot as plt
import os
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from matplotlib import font_manager
from PIL import Image

# フォルダパスを指定
folder_path = "C:/Users/yasud/Documents/src2"
dxf_files = ["test_file1_answer.dxf", "test_file2_answer.dxf"]


for dxf_file in dxf_files:
    dxf_path = os.path.join(folder_path, dxf_file)
    png_path = os.path.join(folder_path, dxf_file.replace(".dxf", ".png"))
    try:
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
        fig.savefig(png_path, dpi=300, bbox_inches='tight')
        plt.close(fig)

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

        img.save(png_path)
        print(f"✅ 画像を保存しました：{png_path}")

    except Exception as e:
        print(f"❌ エラーが発生しました: {dxf_file} : {e}")

print("🎉 DXFファイルをPNGへ変換しました。")