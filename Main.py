import PIL.Image
import PIL.ImageTk
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *

# For x direction
x_kernel = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]

# For y direction
y_kernel = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

# Returns same image
identity = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]

timer_id = None

giflist = "loading.gif"


def avg_color(tuple_input):
    # Average of colors
    return (tuple_input[0] + tuple_input[1] + tuple_input[2]) / 3


def rgb_to_bw(pil_image):
    width = pil_image.size[0]
    height = pil_image.size[1]
    pil_bw_image = Image.new('RGB', (width, height))
    bw_image = pil_bw_image.load()
    rgb_image = pil_image.load()

    # Main loop for conversion from rgb to black
    for i in range(width):
        for j in range(height):
            intensity = avg_color(rgb_image[i, j])
            bw_image[i, j] = (round(intensity), round(intensity), round(intensity))

    return pil_bw_image


def convolve(pil_image, kernel_in):
    kernel_width = len(kernel_in)
    kernel_height = len(kernel_in[1])

    rel_x_kern_index = int(kernel_width / 2)
    rel_y_kern_index = int(kernel_height / 2)

    width = pil_image.size[0]
    height = pil_image.size[1]
    pil_convolve_image = PIL.Image.new('RGB', (width, height))
    convolve_image = pil_convolve_image.load()
    non_convolved_image = pil_image.load()

    # Main convolution loop
    for i in range(width - kernel_width + 1):
        for j in range(height - kernel_height + 1):
            # Inner convolution, move across the kernel, looking at each value in the main image
            sum_all = 0
            for i_k in range(kernel_width):
                for j_k in range(kernel_height):
                    sum_all = sum_all + kernel_in[i_k][j_k] * avg_color(non_convolved_image[i + i_k, j + j_k])

            sum_all = abs(round(sum_all))
            convolve_image[i + rel_x_kern_index, j + rel_y_kern_index] = (sum_all, sum_all, sum_all)

    return pil_convolve_image


def euclidean_norm(pil_image_one, pil_image_two):
    width_one = pil_image_one.size[0]
    height_one = pil_image_one.size[1]

    width_two = pil_image_two.size[0]
    height_two = pil_image_two.size[1]

    if width_one != width_two or height_one != height_two:
        print("INPUT SIZE DOES NOT MATCH euclidean norm")
        return None

    pil_euclidean_norm_image = PIL.Image.new('RGB', (width_one, height_one))
    euclidean_norm_image = pil_euclidean_norm_image.load()

    image_one = pil_image_one.load()
    image_two = pil_image_two.load()

    # Find the euclidean distance between the two arrays at that point
    for i in range(width_one):
        for j in range(height_one):
            intensity = round((avg_color(image_one[i, j]) ** 2 + avg_color(image_two[i, j]) ** 2) ** 0.5)
            euclidean_norm_image[i, j] = (intensity, intensity, intensity)

    return pil_euclidean_norm_image


def sobel_edge():
    x = openfile()
    open_img(x.name)
    pil_input_image = PIL.Image.open(x.name)
    pil_Image_one = convolve(pil_input_image, x_kernel)
    pil_Image_two = convolve(pil_input_image, y_kernel)
    pil_euclidean = euclidean_norm(pil_Image_one, pil_Image_two)

    open_img_src(pil_euclidean)
    pil_euclidean.save(x.name[0:len(x.name) - 4] + "_Sobel.jpg", "JPEG")


def open_img(file):
    # x = openfilename()
    # img = src
    img = PIL.Image.open(file)
    img = img.resize((250, 250), PIL.Image.ANTIALIAS)
    img = PIL.ImageTk.PhotoImage(img)
    panel = Label(root, image=img)
    panel.image = img
    panel.grid(row=2, column=0)


def open_img_src(src):
    img = src
    img = img.resize((250, 250), PIL.Image.ANTIALIAS)
    img = PIL.ImageTk.PhotoImage(img)
    panel = Label(root, image=img)
    panel.image = img
    panel.grid(row=2, column=1)


def openfile():
    file = filedialog.askopenfile(title='"pen')
    return file


def update(ind):
    frame = frames[ind]
    ind += 1
    print(ind)
    if ind > 30:  # With this condition it will play gif infinitely
        ind = 0
    label.configure(image=frame)
    root.after(100, update, ind)


def about():
    toplvl = Toplevel()  # created Toplevel widger
    toplvl.geometry("550x200+300+150")
    Label(toplvl, text="Program yang akan dibuat adalah sebuah implementasi dari algoritma Sobel Edge Detection yang \n"
                       "berfungsi untuk mendeteksi sisi-sisi pada setiap object dalam gambar yang di input. Output\n "
                       "dari program ini adalah berupa gambar hitam putih yang yang menujukan sisi dan garis atau \n"
                       "pola object dalam gambar").grid(row=0, column=0)
    Label(toplvl, text="Anggota Kelompok :").grid(row=4, column=0, columnspan=5)
    Label(toplvl, text="1177050005 Adi Fitrianto").grid(row=5, column=0, columnspan=5)
    Label(toplvl, text="1177050027 Deden Muhamad Furqon").grid(row=6, column=0, columnspan=5)
    Label(toplvl, text="1177050045 Fikry Dzulfikar Rasyid").grid(row=7, column=0, columnspan=5)


if __name__ == "__main__":
    root = Tk()
    root.title("Sobel Edge Detection")
    root.geometry("550x300+300+150")
    root.resizable(width=True, height=True)

    Button(root, text='ABOUT', command=about).grid(row=0, column=0)
    Button(root, text='LOAD IMAGE', command=sobel_edge).grid(row=1, column=0)
    root.mainloop()
