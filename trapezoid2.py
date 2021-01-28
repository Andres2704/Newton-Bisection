def trapezoid(f, a, b, eps, verbose = False):
    '''
    Trapezoidal rule for numerical integration
    f = f(x) to integrate (a function)
    a = initial point 
    b = final point
    eps = tolerance
    verbose = True if it is desired to print the output each iteration
    
    Return:
    Intergral from a to b, relative error, best order(k)
    '''
    # Initializing
    n = 1
    er = 1
    integral = []
    ER = []
    
    # Calculating order zero
    x = [a, b]
    y = list(map(f, x))        
    I = ((b-a)/2)*(y[0] + 2*sum(y[1:-1]) + y[-1])
    integral.append(I)
    
    k = 0
    
    if verbose:
        print('Integral value: ', integral[k])
        print('Relative Error: NaN')
        print('Order: ', k)
        
    while eps < er:
        k = k+1
        # Att the order and x division
        n = 2**k
        h = (b-a)/n
        x = list(np.linspace(a,b,n, endpoint=False))
        x = x + [b]
        # Calculating for all x
        y = list(map(f, x))
        
        # The integral
        I = (h/2)*(y[0] + 2*sum(y[1:-1]) + y[-1])
        integral.append(I)
        
        # Relative Error
        er = abs((integral[k] - integral[k-1])/integral[k-1])
        ER.append(er)
        
        if verbose:
            print('Integral value: ', integral[k])
            print('Relative Error: ', er)
            print('Order: ', k)
            
        
        
    return I, integral,  ER, k

def plot2(I, ER):
    fig, ax = plt.subplots(1,2, figsize=(15,5))
    ax[0].plot(ER, 'o', color='r')
    ax[0].plot(ER)
    ax[0].set_title('Relative error x n')
    ax[1].plot(I, 'o', color='r')
    ax[1].plot(I)
    ax[1].set_title('Integral x n')
    plt.show()
    
def plot(I, ER, save=False):
    xn = [i for i in range(len(I))]
    yy = 1
    xx = 2
    fig = make_subplots(
        rows=yy, cols=xx,
        horizontal_spacing = 0.15
    )
    
    # Layout adjustments
    #fig.update_layout(plot_bgcolor='rgb(255,255,255)')
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_layout(showlegend=False, title_text="Resultados da integração pela regra do trapézio")
    fig.update_layout(font=dict(family="Palatino Linotype",size=12,color="Black"))
    
    # Integral plot
    fig.add_trace(go.Scatter(x=xn, y=I , marker=dict(
                color='royalblue',
                line_width=0.5
            )), row=1, col=1)
    fig.update_xaxes(title_text="Ordem", row=1, col=1)
    fig.update_yaxes(title_text="Valor integral [UA]", row=1, col=1)
    
    # Relative error plot
    fig.add_trace(go.Scatter(x=xn[1::], y=ER, marker=dict(
                color='red',
                line_width=0.5
            )), row=1, col=2)
    fig.update_xaxes(title_text="Ordem", row=1, col=2)
    fig.update_yaxes(title_text="Erro relativo", row=1, col=2)
    
    if save:
        fig.write_image("resultado_integracaotrapezio.png")
    
    fig.show()

def to_df(I, ER, name = 'P_IntegracaoNumerica.xlsx', save=False):
    ER = [''] + ER
    df = pd.DataFrame(columns = 'Integral;Erro Relativo'.split(';'))
    df['Integral'] = I; df['Erro Relativo'] = ER;
    if save: df.to_excel(name)
    return df
    
eps = 1.0E-6
a = -1.0
b = 1.0

I, integral, ER, n = trapezoid(lambda x: 1/(x+2), a, b, eps, verbose=False)
plot(integral, ER, save=True)
df = to_df(integral, ER, save=True)
