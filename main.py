import cv2

ksi = -600, 550 #Погрешность

k1=1483, 24
k2=7671, 1100
k3=6300,7112
k4=39,6023

TOWN = 42.48425110546248,27.443847656250004,'Burgas'
#TOWN = 40.97056664236637, 27.938919067382816,'Marmara'

def pase(corner):
    inp = open('LE07_L1TP_181031_20020917_20170128_01_T1_MTL.txt').readlines()
    for i in iter(inp):
        if corner in i:
            original = i[4:]
            return float(original.replace(corner + " = ", ""))

def pointCalculate(a,b,K):

    lambd = K / (1 - K)
    if lambd <= 0.5:
        x = int((a[0] + lambd * b[0]) / (1 + lambd))
        y = int((a[1] + lambd * b[1]) / (1 + lambd))
        return x,y
    else:
        lambd = 1 / lambd
        x = int((b[0] + lambd * a[0]) / (1 + lambd))
        y = int((b[1] + lambd * a[1]) / (1 + lambd))

        return x,y

C_UL = pase('CORNER_UL_LAT_PRODUCT'), pase('CORNER_UL_LON_PRODUCT')
C_UR = pase('CORNER_UR_LAT_PRODUCT'), pase('CORNER_UR_LON_PRODUCT')
C_LL = pase('CORNER_LL_LAT_PRODUCT'), pase('CORNER_LL_LON_PRODUCT')
C_LR = pase('CORNER_LR_LAT_PRODUCT'), pase('CORNER_LR_LON_PRODUCT')

deltaLatitude = abs((C_UL[0] + C_UR[0]) / 2 - (
            C_LL[0] + C_LR[0]) / 2)
deltaLongitude = abs(
   (C_UL[1] + C_LL[1]) / 2 - (C_UR[1] + C_LR[1]) / 2)

coeff1 = abs((abs((C_UL[1] + C_LL[1]) / 2) - abs(TOWN[1])) / deltaLongitude)
coeff2 = abs((TOWN[0] - (C_LL[0] + C_LR[0]) / 2) / deltaLatitude)

SOLVE = int(pointCalculate(k1,k2,coeff1)[0]+ ksi[0]),int(pointCalculate(k4,k1,coeff2)[1]+ksi[1])

img = cv2.imread("LE07_L1TP_181031_20020917_20170128_01_T1_B1.TIF")

img = cv2.line(img, (SOLVE[0]-1000,SOLVE[1]+1000), (SOLVE[0]+1000, SOLVE[1]+1000), (0,0,255), 15)
img = cv2.line(img, (SOLVE[0]+1000,SOLVE[1]-1000), (SOLVE[0]-1000, SOLVE[1]-1000), (0,0,255), 15)

img = cv2.line(img, (SOLVE[0]+1000,SOLVE[1]+1000), (SOLVE[0]+1000, SOLVE[1]-1000), (0,0,255), 15)
img = cv2.line(img, (SOLVE[0]-1000,SOLVE[1]+1000), (SOLVE[0]-1000, SOLVE[1]-1000), (0,0,255), 15)

cv2.putText(img,TOWN[2],(SOLVE[0]-350, SOLVE[1]),cv2.FONT_HERSHEY_SIMPLEX,8,(0,0,255),10)

result = img
screen_res = 1920, 1080
scale_width = screen_res[0] / result.shape[1]
scale_height = screen_res[1] / result.shape[0]
scale = min(scale_width, scale_height)
window_width = int(result.shape[1] * scale)
window_height = int(result.shape[0] * scale)

cv2.namedWindow('MyWind', cv2.WINDOW_NORMAL)
cv2.resizeWindow('MyWind', window_width, window_height)

cv2.imshow('MyWind', result)
cv2.waitKey(0)
cv2.destroyAllWindows()


