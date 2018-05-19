import os
# while True:
def build_gpu_html():
    f = open('./gpu_states/p40gpu_output.txt')
    data = f.readlines()
    f.close()
    new_data = [item+"<br>" for item in data]

    pre = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="refresh" content="3">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>GPU Venus</title>
    </head>
    <body><pre>"""
    #     <meta http-equiv="refresh" content="2">

    post = """</pre><div id="aa"></div>
    <script language="javascript">
    var fso, ts, s ;
    var ForReading = 1;
    fso = new ActiveXObject("Scripting.FileSystemObject");
    ts = fso.OpenTextFile("/var/www/html/syzhang/sync_gpu/output.txt", ForReading);
    s = ts.ReadLine();
    document.getElementById("aa").innerHTML=s;
    </script>
    </body>
    </html>"""

    if os.path.exists('p40gpu.html'):
        os.remove('p40gpu.html')
    f_html = open('p40gpu.html', 'a')
    f_html.write(pre)
    f_html.writelines(data)
    f_html.write(post)

    f_html.close()

    #import time
    #time.sleep(3)

