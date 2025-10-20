
def change_origin_image(df, img_size): 
  df['field_x'] = df['field_x'] - img_size['width']/2
  df['field_y'] = -(df['field_y'] - img_size['height']/2)
  return df

