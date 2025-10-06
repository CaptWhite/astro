import numpy as np
import pandas as pd

from app.services_calculate._rutines import degree_to_radian

def calculate(ar, dec, x, y):
  X3 = x*x*x
  X2Y = x*x*y
  XY2 = x*y*y
  Y3 = y*y*y
  X2 = x*x
  XY = x*y
  Y2 = y*y
  X = x
  Y = y
  ind = np.ones(x.size) 
 
  # Creamos la matriz de diseño X
  MX = np.column_stack((X3, X2Y, XY2, Y3, X2, XY, Y2, X, Y, ind))

  # Calculamos los coeficientes usando la fórmula de mínimos cuadrados
  a_est_AR = np.linalg.inv(MX.T @ MX) @ MX.T @ ar
  a_est_DEC = np.linalg.inv(MX.T @ MX) @ MX.T @ dec
  return [a_est_AR, a_est_DEC] 


def calculate_plate(df, img_size):
  arr_ar = df['ar_app'].to_numpy()
  arr_dec = df['dec_app'].to_numpy()
  # arr_x = df['field_x'].to_numpy()
  # arr_y = df['field_y'].to_numpy()
  arr_x = df['field_x'].to_numpy() - img_size['width']/2
  arr_y = -(df['field_y'].to_numpy() - img_size['height']/2)
  [pc_ar, pc_dec] = calculate(arr_ar, arr_dec, arr_x, arr_y)
  coefs_name = ['X³', 'X²Y', 'XY²', 'Y³', 'X²', 'XY', 'Y²', 'X', 'Y', 'ind'] 
  coefs = pd.DataFrame({
    'Coef': coefs_name,
    'AR': degree_to_radian(pc_ar),
    'DEC': degree_to_radian(pc_dec)
  })


  def calculate_residues(ra, dec, x, y, pc_ar, pc_dec):
    ar_res = ra - (
      (pc_ar[0] * x * x * x) + (pc_ar[1] * x * x * y) + (pc_ar[2] * x * y * y) + (pc_ar[3] * y * y * y) + 
      (pc_ar[4] * x * x) + (pc_ar[5] * x * y) + (pc_ar[6] * y * y) + 
      (pc_ar[7] * x) + (pc_ar[8] * y) + 
       pc_ar[9]) 
    
    dec_res = dec - (
      (pc_dec[0] * x * x * x) + (pc_dec[1] * x * x * y) + (pc_dec[2] * x * y * y) + (pc_dec[3] * y * y * y) + 
      (pc_dec[4] * x * x) + (pc_dec[5] * x * y) + (pc_dec[6] * y * y) + 
      (pc_dec[7] * x) + (pc_dec[8] * y) + 
       pc_dec[9])
    return [ar_res, dec_res]

  df[['ra_resid', 'dec_resid']] = df.apply(lambda row: calculate_residues(degree_to_radian(row['ar_app']), degree_to_radian(row['dec_app']), row['field_x'], row['field_y'], degree_to_radian(pc_ar), degree_to_radian(pc_dec)), axis=1, result_type='expand')
  return df, coefs
