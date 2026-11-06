def create_diagonal_gradient(canvas,koji, width, height):
    if(koji==1):
        end_rgb = (4, 2, 13)
        start_rgb = (20, 0, 150)
    elif(koji==2):
        end_rgb = (4, 13, 2)
        start_rgb = (20, 150, 0)
    else:
        end_rgb = (13, 2, 4)
        start_rgb = (150, 0, 20)
    step = 2
    for i in range(0, width + height, step):
        ratio = i / (width + height)
        
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
        
        color = f'#{r:02x}{g:02x}{b:02x}'
        
        canvas.create_line(i, 0, 0, i, fill=color, width=step)
        