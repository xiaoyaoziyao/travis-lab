from numpy import *
from PIL import Image
import time

def image_to_dat(image_file, dat_file):
    img = Image.open(image_file)
    # Convert from RGB to grayscale (0..255)
    img = img.convert('L')
    np_img = array(img)
    # Invert image. Each value set to 255 - value.
    # Black (0) pixels, become 1. White (255) pixels become 0.
    np_img = invert(np_img)
    # Set non-white (non 0) pixels to black.
    np_img[np_img > 0] = 1
    (height, width) = np_img.shape
    header = "%d %d" % (width, height)
    savetxt(dat_file, np_img, fmt="%d", header=header, comments="")
    return np_img

def dat_to_data(dat_file):
    #Get array of the landscape
    data_array = genfromtxt(dat_file, skip_header = 1)
    #Get shape of the landscape
    #(height, width)
    data_shape = data_array.shape
    return(data_shape,data_array)

def initial_rand(data_shape,land_array):
    den_array = random.random(data_shape) * 5.0
    den_array[land_array == 0] = 0.
    return den_array

def sum_neighbours(data_array,land_array):
    data_shape = shape(data_array)
    #Creating a copy of the data_array with a halo of zeroes
    zeros_side = zeros((data_shape[0],1))
    zeros_top = zeros((1,data_shape[1]+2))
    middle_block = block([zeros_side, data_array, zeros_side]) 
    halo = block([[zeros_top],
                         [middle_block],
                         [zeros_top]
                         ])
    # This will be the array that will be returned later on
    output_array = zeros(data_shape)
    # Summing of the neighbours starts below
    for i in range(data_shape[0]):
        for j in range(data_shape[1]):
                output_array[i][j] = halo[i][j+1] + halo[i+2][j+1] + halo[i+1][j+2] + halo[i+1][j]
    output_array[land_array == 0] = 0.
    return output_array

def output_PPM(H,P,ppm_name):
    width = shape(H)[1]
    height = shape(H)[0]
    maxval = 255
    ppm_header = f'P6 {width} {height} {maxval}\n'
    with open(ppm_name, 'wb') as f:
        f.write(bytearray(ppm_header, 'ascii'))
        H.tofile(f)

def average(H):
    aver=sum(sum(H[i]) for i in range(len(H)))/H.shape[0]/H.shape[1]
    return aver
    
def PumaHares(a,b,r,k,l,m,dt,T,image_file):
    
    # Start timing
    start = time.time()
    # getting the binary array and shape
    dat_file="F:/【coursework】/【11.07】-70% (Python) Programming Skills/coursework-development/1.bat"
    image_to_dat(image_file, dat_file)
    land_data = dat_to_data(dat_file)
    
    # shape of the landscape
    land_shape = land_data[0]
    # binary array of the landscape
    land_array = land_data[1]
    # initializing the density of Hares and Puma
    H = initial_rand(land_shape,land_array)
    P = initial_rand(land_shape,land_array)
    print(H,P)
    # output the ppm files here
    output_PPM(H,P,'ppm_0.0.ppm')
        # Put ppm functions here!
    # Number of "dry" neighbours for each grid square
    dry_neighbours = sum_neighbours(land_array,land_array)
    # Initialise the time t and count for T timing to the next time interval
    t, checker = dt, 1
    while t < 500.:
        d = round(t/dt)/4
        HP = H*P
        H = H + dt*(r*H - a*HP + k*(sum_neighbours(H,land_array) - dry_neighbours * H))
        P = P + dt*(b*HP - m*P + l*(sum_neighbours(P,land_array) - dry_neighbours * P))
        if checker == T:
            ppm_name = 'ppm_'+str(d)+'.ppm'
            output_PPM(H,P,ppm_name)
            #ppm function here!
            checker = 0
        checker += 1
        t += dt
    end = time.time()
    print( "The total time taken for the simulation is", (end - start) ) 


imagefile="random.bmp"
PumaHares(0.04,0.02,0.08,0.2,0.2,0.06,0.4,4,imagefile)
