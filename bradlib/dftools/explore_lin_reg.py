def explore_lin_reg(df,y_var,x_var,plotting=False,ols_output=False,model_check=False,nbins=20):
    """
    Function to explore OLS regression graphically and calculate results for a particular variable and time period (year).
    Input args:
    df: data to investigate; pandas df
    y_var: column name; string (df column name)
    x_var: explanatory varaible of interest; string (df column name)
    
    plotting: if True show regression plots
    ols_output: if True print linear regression output tables
    model_check: if True show model check plots
    
    nbins: set bins for hist plots (optional) 
    """
    
    import statsmodels.formula.api as smf
    import statsmodels.api as sm
    import patsy
    import matplotlib.pyplot as plt
    import numpy as np
    
    #### conduct regression
    ## y_var
    lm1 = []
    lm1 = smf.ols(formula= y_var +' ~ ' + x_var, data=df).fit()
    x1=[]
    x1 = patsy.dmatrix(x_var, data=df)
    preds1 = []
    preds1 = lm1.predict(x1, transform=False)
    
    ## extract cook's D values
    lm1_cd = lm1.get_influence().cooks_distance[0]
    
    if plotting == True:
        #### Make plots
        fig1 = plt.figure(figsize=(10,8))

        #### y_var
        ## scatter and regression line for y_var
        ax1 = plt.subplot(221)
        ax1.scatter(x=df[x_var], y = df[y_var])
        ax1.plot(x1[:,1],preds1,c='red') #### [:,1] removes the constant line at x = 1.0
        ax1.set_xlabel(x_var)
        ax1.set_ylabel(y_var)

        ## histogram for y_var
        ax2 = plt.subplot(222)
        ax2 = df[y_var].plot(kind = 'hist', bins = nbins)
        ax2.axvline(df[y_var].median(),color= 'r',label='median')
        ax2.set_xlabel(y_var)
        ax2 = df[y_var].plot(kind='kde', grid=False,label='KDE')

        #### x_var
        ## histogram for x_var
        ax3 = plt.subplot(223)
        ax3 = df[x_var].plot(kind = 'hist', bins = nbins)
        ax3.axvline(df[x_var].median(),color= 'r',label='median')
        ax3.set_xlabel(x_var)
        ax3 = df[x_var].plot(kind='kde', grid=False,label='KDE')
        
        #### OLS output
        cd_thresh = 0.5
        ## set up axes and then clear it all
        ax4 = plt.subplot(224)
        ax4.clear()
        ax4.set_xticklabels([])
        ax4.set_yticklabels([])
        ax4.grid()
        ax4.set_facecolor((1, 1, 1))

        #### add details of regression to plot
        ax4.annotate('R-value:',xy=(0,0.9),fontsize=16)
        ax4.annotate(lm1.rsquared.round(3) ,xy=(0.3,0.9),fontsize=15 )
        
        ax4.annotate('P-value:',xy=(0.7,0.9),fontsize=16)
        ax4.annotate("{:.4f}".format(lm1.pvalues.loc[x_var]) ,xy=(0.95,0.9),fontsize=15 )
        
        ax4.annotate('Model values:', xy=(0,0.7),fontsize=18)
        ax4.annotate(lm1.params.keys()[0] + ': ' + np.str(lm1.params.values.round(3)[0])
                     ,xy = (0,0.55),textcoords='axes fraction',fontsize=14)
        ax4.annotate(lm1.params.keys()[1] + ': ' + np.str(lm1.params.values.round(3)[1])
                     ,xy = (0,0.45),textcoords='axes fraction',fontsize=14)
        
        ax4.annotate('Conf intervals:',xy=(0.7,0.7),fontsize=18)
        ax4.annotate(lm1.conf_int().values.round(3)[0],xy = (0.7,0.55),textcoords='axes fraction',fontsize=14)
        ax4.annotate(lm1.conf_int().values.round(3)[1],xy = (0.7,0.45),textcoords='axes fraction',fontsize=14)
        
        ax4.annotate("high Cook's-D val: " + str(len(lm1_cd[np.where(lm1_cd > cd_thresh)])),xy=(0,0.1),fontsize=14)

    #### print regression details
    if ols_output == True:
        print(lm1.summary2())
    
    #### produce model checking plots
    if model_check == True:
        fig2 = plt.figure(figsize=(15,4))
        ## residuals plot
        ax8 = plt.subplot(131)
        plt.scatter(lm1.fittedvalues,lm1.resid,color='b',s=20,alpha=0.4)
        plt.plot([lm1.fittedvalues.min(),lm1.fittedvalues.max()],[0,0],color='r')
        ax8.set_xlabel('Fitted values')
        ax8.set_ylabel('Residuals')
        ax8.autoscale(enable=True,tight=True)
        
        ## qq ploting
        ax9 = plt.subplot(132)
        sm.graphics.qqplot(lm1.resid.values ,line='s',fit=True,ax=ax9)
        
        ## Cooks D
        ax7 = plt.subplot(133)
        ax7.bar(np.arange(len(lm1_cd)),lm1_cd,color='b')
        ax7.set_ylabel("Cook's distance")
        
        
    return(lm1)