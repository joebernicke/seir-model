import numpy as np
from scipy.integrate import odeint
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt
def create_array(t):
    susceptible=np.zeros((len(t),1))
    infected=np.zeros((len(t),1))
    removed=np.zeros((len(t),1))
    exposed=np.zeros((len(t),1))

def model(x,t,gamma,alpha,rho,contact_rate):
   susceptible=x[0];
   exposed=x[1];
   infected=x[2];
   removed=x[3];
   dsdt=-susceptible*contact_rate*infected*rho # Units= 
                       #change in people susceptible to the disease and is moderated by
                       #the number of infected people and their contact with the infected.

   dedt=rho*susceptible*infected*contact_rate-exposed*alpha

                       #gives the people who have been exposed to but not yet infected 
                       #the disease. It grows based on the contact rate and decreases based on the
                       #incubation period whereby people then become infected. 

   didt=alpha*exposed-gamma*infected
                       #gives us the change in infected people based on the exposed population and
                       #the incubation period. It decreases based on the infectious period, so
                       #the higher γ is, the more quickly people die/recover 
   drdt=gamma*infected
                       #Rate at which people die or recover

   N=susceptible+exposed+infected+removed
                       #Ensures that the total number of people is always constant.
   return [dsdt,dedt,didt,drdt]

def get_model(init_cond,t,gamma,alpha,rho,contact_rate):
    rate= odeint(model,init_cond,t,args=(gamma,alpha,rho,contact_rate))
    #Dump Data into lists
    infected=rate[:,2]
    susceptible= rate[:,0]
    exposed=rate[:,1]
    removed=rate[:,3]
    return susceptible,exposed,infected,removed 
    
def get_max(*arg):
        maxElement=np.amax(arg)
        result=np.where(arg==np.amax(arg))
        number_dead=maxElement*330000*.01        
        top=str(round(maxElement*330,2))+'m Infected'+' ---- '+str(round(number_dead)) + "k Dead"
        return maxElement,result,top,number_dead

def update():
    #get_slider(init_cond,t,gamma,alpha,rho,contact_rate)
    #cont_slider,rho_slider,alpha_slider,gamma_slider=get_slider(init_cond,t,gamma,alpha,rho,contact_rate)
    ann[0].remove()

    Q=get_max(odeint(model,init_cond,t
                     ,args=(gamma_slider.val,alpha_slider.val,rho_slider.val,cont_slider.val))[:,2])

    ann[0]=plot2.annotate(Q[2],xy=(t[Q[1][1]][0], Q[0]), xytext=(.40, .75), xycoords='figure fraction')
    lin2.set_ydata(odeint(model,init_cond,t,args=(gamma_slider.val,alpha_slider.val,rho_slider.val,
                                                  cont_slider.val))[:,2])
    fig2.canvas.draw_idle()   
    
def get_slider(init_cond,t,gamma,alpha,rho,contact_rate):
    cont_slider=Slider(plt.axes([.22, .125, 0.25,.025]),'contact_rate',0,5,valinit=contact_rate)
    rho_slider=Slider(plt.axes([.22, .098, 0.25,.025]),'Human fac',0,1,valinit=rho)
    alpha_slider=Slider(plt.axes([0.65, 0.125, 0.25,.025]),'1/(t_inc)',0,1,valinit=alpha)
    gamma_slider=Slider(plt.axes([0.65, .098, 0.25,.025]),'1/(t_inf)',0,1,valinit=gamma)
    #Q=get_max(odeint(model,init_cond,t,args=(gamma_slider.val,alpha_slider.val,rho_slider.val,cont_slider.val))[:,2])
    #ann=[plt.annotate(Q[2],xy=(t[Q[1][1]][0], Q[0]), xytext=(t[Q[1][1]][0]+30, Q[0]),
                 #arrowprops=dict(facecolor='black', shrink=0)
 #)]
    
    return cont_slider,rho_slider,alpha_slider,gamma_slider
    
