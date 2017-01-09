from numpy import cos,linspace,exp
# import matplotlib.pyplot as plt
import bokeh.plotting as plt

import os,time,glob,re

def damped_vibrations(A,w,b,t):
    return A*exp(-b*t)*cos(w*t)



def compute(A,w,b,T, resolution = 500):
    """Return filename of plot of the damped_vibration function."""
    t = linspace(0,T,resolution+1)
    u = damped_vibrations(A,w,b,t)
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select,lasso_select"
    p = plt.figure(title="simple line example", tools=TOOLS,
                   x_axis_label='t', y_axis_label='y')

    # add a line renderer with legend and line thickness
    p.line(t, u, legend="u(t)", line_width=2)

    from bokeh.resources import CDN
    from bokeh.embed import components
    script, div = components(p)
    head = """
<link rel="stylesheet"
 href="http://cdn.pydata.org/bokeh/release/bokeh-0.12.3.min.css"
 type="text/css" />
<script type="text/javascript"
 src="http://cdn.pydata.org/bokeh/release/bokeh-0.12.3.min.js">
</script>
<script type="text/javascript">
Bokeh.set_log_level("info");
</script>
"""
    return head, script, div
    # plt.figure() # needed to avoid adding curves in plot???
    # plt.plot(t,u)
    # plt.title('A=%g,w=%g,b=%g'%(A,w,b))
    # if not os.path.isdir('static'):
    #     #if the directory does not exist ,make one
    #     os.mkdir('static')
    # else:
    #
    #      for filename in glob.glob(os.path.join('static','*png')):
    #          os.remove(filename)
    #
    # plotfile = os.path.join('static',str(time.time())+'.png')
    # plt.savefig(plotfile)
    # return  plotfile
if __name__=="__main__":
    print compute(A=1, b=0.2, w=6.28,  resolution=500)

