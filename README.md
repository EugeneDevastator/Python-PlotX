# PlotX

Simple usage library to plot graphs and easily decript arrays for that purpose.

Expample Usage:

```python
import plotx

data=[[1,10],[2,20]]

plotx.dots(data,"*xy")
plotx.dots(data,"*x,*y")
```

*xy will unfold like x=1,y=10 ; x=2,y=20
*x,*y will unfold like x=1,y=2 ; x=10,y=20

