import numpy as np
import pandas as pd

from app.services_calculate._rutines import degree_to_radian

def calculate_MX(ar, dec, x, y):
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
  return MX

def calculate_coeficients(MX, ar, dec, x, y):  
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
  MX = calculate_MX(arr_ar, arr_dec, arr_x, arr_y) 
  [pc_ar, pc_dec] = calculate_coeficients(MX, arr_ar, arr_dec, arr_x, arr_y)
  coefs_name = ['X³', 'X²Y', 'XY²', 'Y³', 'X²', 'XY', 'Y²', 'X', 'Y', 'ind'] 
  coefs = pd.DataFrame({
    'Coef': coefs_name,
    # 'AR': degree_to_radian(pc_ar),
    # 'DEC': degree_to_radian(pc_dec)
    'AR_deg': pc_ar,
    'DEC_deg': pc_dec,
    'AR_rad': degree_to_radian(pc_ar),
    'DEC_rad': degree_to_radian(pc_dec)
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
    return [ar_res, dec_res, degree_to_radian(ar_res), degree_to_radian(dec_res)]

  def calculate_variance(MX, ar_res_deg, dec_res_deg):
    # V_deg = np.vstack((ar_res_deg, dec_res_deg))
    # V_deg = V_deg.flatten()
    num_coefs = MX.shape[1]
    #n_observ = V_deg.size
    n_observ = ar_res_deg.size
    grados_libertad = n_observ - num_coefs
    # suma_cuadrados_residuos = np.dot(V_deg.T, V_deg)
    suma_cuadrados_residuos_ar = np.dot(ar_res_deg.T, ar_res_deg)
    suma_cuadrados_residuos_dec = np.dot(dec_res_deg.T, dec_res_deg)
    sigma0_sq_ar = suma_cuadrados_residuos_ar / grados_libertad
    sigma0_sq_dec = suma_cuadrados_residuos_dec / grados_libertad

    COV_matrix_ar = sigma0_sq_ar * np.linalg.inv(MX.T @ MX)
    COV_matrix_dec = sigma0_sq_dec * np.linalg.inv(MX.T @ MX)
    variance_ar_deg = np.diag(COV_matrix_ar)
    variance_dec_deg = np.diag(COV_matrix_dec)
    variance_ar_rad = variance_ar_deg * (np.pi/180)**2
    variance_dec_rad = variance_dec_deg * (np.pi/180)**2
    return [variance_ar_deg, variance_ar_rad, variance_dec_deg, variance_dec_rad]


  # df[['ra_resid', 'dec_resid']] = df.apply(lambda row: calculate_residues(degree_to_radian(row['ar_app']), degree_to_radian(row['dec_app']), row['field_x'], row['field_y'], degree_to_radian(pc_ar), degree_to_radian(pc_dec)), axis=1, result_type='expand')
  df[['ra_resid_deg', 'dec_resid_deg', 'ra_resid_rad', 'dec_resid_rad']] = df.apply(lambda row: calculate_residues(row['ar_app'], row['dec_app'], row['field_x'], row['field_y'], pc_ar, pc_dec), axis=1, result_type='expand')

  resultados = calculate_variance(MX, df['ra_resid_deg'], df['dec_resid_deg'])
  #coefs[['variance_deg', 'variance_rad']] = resultados     # Serie completa de Pandas (array)
  coefs['variance_ar_deg'] = resultados[0]
  coefs['variance_ar_rad'] = resultados[1]
  coefs['variance_dec_deg'] = resultados[2]
  coefs['variance_dec_rad'] = resultados[3]
  return df, coefs
