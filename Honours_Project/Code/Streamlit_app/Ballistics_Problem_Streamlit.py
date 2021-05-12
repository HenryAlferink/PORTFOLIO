import streamlit as st
import numpy as np
from scipy.linalg import sqrtm
import matplotlib.pyplot as plt
import matplotlib

# streamlit needs this for matplotlib
from matplotlib.backends.backend_agg import RendererAgg
_lock = RendererAgg.lock

# plt.rcParams.update({'font.size': 18})
matplotlib.rcdefaults()

st.sidebar.markdown("""
# Setting modification
Feel free to change these.
""")
st.sidebar.markdown(r"### Number of data points")
m = st.sidebar.slider(
    "",
    min_value=3,
    max_value=50,
    value=25,
    step=1
)
st.sidebar.markdown(r"### Data standard deviation $\mathbf{C}_D$")
data_stddev = st.sidebar.slider(
    "",
    min_value=1,
    max_value=1000,
    value=300
)
st.sidebar.markdown(r"### Prior standard deviation scale $c$")
c = st.sidebar.slider(
    "",
    min_value=0.001,
    max_value=2.,
    value=1.
)
st.sidebar.markdown(r"""
---
Please reload this page to reset to default values.

---
**Author**: Henry Alferink
""")

st.markdown("""
# Ballistics Problem Inversion

Here we show two different methods of finding the solution to an inverse problem: the least squares method in the frequentist framework, and a method that uses the Bayesian framework. 

Feel free to change the parameters in the sidebar, and watch the output change below.

## Model and data
A simple projectile motion model can be expressed as
$$
y(t) = m_1 + m_2 t - \\frac{1}{2}m_3 t^2,
$$ 
where $y(t)$ is the height of a projectile at time $t$. Along with this mathematical model we also have actual gathered data. We assume that the data has normally distributed noise. Therefore, the data can be expressed in equation form (adjust the standard deviation in the sidebar!):
$$
d_i = y(t_i) + \\varepsilon_i, \\hspace{1cm} \\varepsilon_i \\overset{iid}{\\sim} N(\\mu =0, \\sigma_D=%s).
$$
$$
\\vphantom{.}
$$
The model is linear in its parameters, so we can express it as $\mathbf{d} = \mathbf{Gm}+\mathbf{\\varepsilon}$ where
$$
\mathbf{m}=\\begin{bmatrix}m_1 & m_2 & m_3\\end{bmatrix}^T,
$$
and the design matrix is
$$
G_{i,.} = \\begin{bmatrix}1 &t_i & -(1/2)t_i^2\end{bmatrix}.
$$

For the purpose of our example, we will take $$\\mathbf{m}_{true}=\\begin{bmatrix}600 & 100 & 9.8\\end{bmatrix}^T$$ to be the true parameter set. This is what we use to create our simulated dataset. In the real world we won't know $\mathbf{m}_{true}$.

The *inverse problem* is this: we want to solve for $\mathbf{m}$. In the general case, we would need a method such as gradient descent to find parameters such that the residuals are minimized. However, since our mathematical model is linear in its parameters, we are able to find the the parameter solution analytically--in both the frequentist and Bayesian frameworks. 
""" % (
    data_stddev
    ))

# true params
m_true = np.array([600, 100, 9.8])

# time steps
t = np.arange(1,m+1)

st.markdown("""
## Solving using Least Squares in the Frequentist Framework
If we use the *least squares* critera as our functional to minimize, i.e.
$$
\\text{minimize} \sum_i (d_i - y(t_i))^2
$$

then we have an analytical solution
$$
\\mathbf{m}_{leastsquares} = (\mathbf{G}^T\mathbf{G})^{-1}\mathbf{G}^T\mathbf{d}.
$$
This is called the *normal equation*. After taking the model output that results from using these parameters, we can plot the results and compare the model result to the data. For the sake of example the true motion is also plotted; however, in the real world we will never know this.
# """)


# function
def f(time, model): 
    return model[0] + model[1]*time - 0.5*model[2]*time**2 


# the second argument is std. deviation, not variance.
d = f(t, m_true) + np.random.normal(0, data_stddev, m) 

# design matrix
G = np.zeros((m, 3))
for i in range(m):
    G[i,:] = [1, t[i], -0.5*t[i]**2]

# least squares solution
m_ls = np.linalg.inv(G.T@G)@G.T@d

with _lock:
    fig, ax = plt.subplots(figsize=(6.50127, 3))
    l1, = ax.plot(t, d, '.', label='Data $\mathbf{d}$', c='k')
    l2, = ax.plot(t, f(t, m_ls), label="Least Squares Estimate $\mathbf{Gm}_{leastsquares}$", c='tab:orange')
    l3, = ax.plot(t, f(t, m_true), label="True Motion $\mathbf{Gm}_{true}$", c='k')
    ax.set_xlabel('Time')
    ax.set_ylabel('Height')
    fig.tight_layout()

    fig.subplots_adjust(bottom=0.3, wspace=0.33)
    ax.legend(handles=[l1, l2, l3], loc='upper center', 
        bbox_to_anchor=(0.5, -0.25), shadow=False)

    st.pyplot(fig)

st.markdown("""
If we have enough data points, the least squares solution can be quite good (change the number of data points in the side bar!). Actually, this balistics problem in general seems to be rather well-posed, so it is relatively easy to get a good solution (I should have chosen a different example!). However, it is not always possible to get good results using the least squares solution (?). In this case, regularization methods such as Tikhonov regularization need to be used. 

*Or*, we can solve the problem in the Bayesian framework, which in a sense regularizes the solution through the subjective choice of a *prior distribution*. This prior distribution is essentially a subjective guess as to what the solution should be, which, while not perfect, will provide some helpful constraining to the final solution.

## Solving using the Bayesian framework
The least squares solution above was found using the *frequentist framework*. This framework assumed that the true parameters were fixed. We now try to solve for the parameters in the Bayesian framework. Here we assume the parameters to be probability distributions rather than fixed values. In the Bayesian framework, we call our initial guess of the parameters the *prior distribution*. From here we essentially *update* the prior by applying the data. This produces the Bayesian solution, called the *posterior distribution*. Note that in the Bayesian framework we can no longer refer to the *true parameter*; rather, if we want to refer to some particular value, we will have to use something like the *mean* of the distribution. Therefore, in the plots below, you'll see reference to the *true mean* rather than the *true parameter*.

Assuming that the data is iid normal distributed, the data covariance matrix will look like
$$
\mathbf{C}_D = \sigma_d^2 \mathbf{I}_{m},
$$
where $\mathbf{I}_m$ is the $m \\times m$ identity matrix (m is the number of data points).
""")

# data covariance
C_D = data_stddev**2 * np.eye(m)

st.markdown("""
Recalling that the prior is our initial guess. We will take the _prior mean_ to be 
$$
\mathbf{m}_{prior} = \\begin{bmatrix}800 & 0 & 0\\end{bmatrix}^T
$$ 
this produces a constant function.

Now, when it comes to choosing the prior, we will ideally want to use variances (diagonal entries, each on corresponding to one of the 3 parameters) such that the true parameter means lie somewhere in the range of one standard deviation from the prior mean. This may be difficult to do in practice, so it can be better to choose a larger value here to be on the safe side; however, the smaller we can make these (while staying consistent), the more accurate our final solution will be! The prior covariance we will use is shown below. Notice that the size of the diagonal entries are somewhat proportional to the corresponding value in our choice of prior mean. 
""")
st.latex(r"\mathbf{C}_{prior} = c \begin{bmatrix}40000 & 0 & 0 \\  0 & 10000 & 0 \\  0 & 0 & 100 \end{bmatrix},")
st.markdown(r"""
$c$ is a scaling constant. Feel free to change this in the sidebar!

In the case of a normally distributed prior and normally distributed data noise, it can be shown that the posterior distribution will also be normally distributed. Therefore, we need to find the posterior mean and covariance. It can be shown (reference?) that the posterior mean is found using
$$
\mathbf{m}_{MAP} = \underset{\mathbf{m}}{\text{argmin}}\left|\left| \mathbf{Am} - \mathbf{b} \right|\right|_2^2
$$
where
$$
\mathbf{A} = \begin{bmatrix} 
    \mathbf{C}_D^{-1/2}\mathbf{G}\\
    \mathbf{C}_{prior}^{-1/2}
\end{bmatrix}
$$
and
$$
\mathbf{b} = \begin{bmatrix} 
    \mathbf{C}_D^{-1/2}\mathbf{d}\\
    \mathbf{C}_{prior}^{-1/2}\mathbf{m}_{prior}
\end{bmatrix}.
$$
But, this looks exactly like a least squares problem; therefore, we can use the following to find the posterior mean. However, note that we are certainly not working in the frequentist framework here! Because of the assumption we have made, it just happens to be a similar looking equation.
$$
\mathbf{m}_{MAP} = (\mathbf{A}^T\mathbf{A})^{-1} \mathbf{A}^T \mathbf{b}
$$

The posterior covariance is found by taking
$$
\mathbf{C}_{post} = \left( \mathbf{G}^T \mathbf{C}_D^{-1} \mathbf{G} + \mathbf{C}_{prior} \right)^{-1}.
$$

We now have our solution, that is, the posterior distribution! Below we plot the posterior of each parameter individually. Notice how we start with our prior distribution, and the posterior is, in a sense, *updated* after applying the data. Ideally, we always want the (hypothetical) true mean to be encompassed within the bounds of the posterior distribution. In other words, ideally, the posterior should always be closer to the true mean than the prior.
""")

# m_prior = np.array([550, 110, 5])
m_prior = np.array([800, 0, 0])

C_M = c * np.diag([40000, 10000, 100])

A = np.concatenate(
    [np.linalg.inv(sqrtm(C_D)) @ G,
     np.linalg.inv(sqrtm(C_M))]
)
b = np.concatenate(
    [np.linalg.inv(sqrtm(C_D)) @ d,
     np.linalg.inv(sqrtm(C_M)) @ m_prior]
)

m_map = np.linalg.inv(A.T @ A) @ A.T @ b

C_M_p = np.linalg.inv(G.T @ np.linalg.inv(C_D) @ G + np.linalg.inv(C_M))

st.markdown(r"""

""")

post_dist = np.random.multivariate_normal(m_map, C_M_p, size=1000)
prior_dist = np.random.multivariate_normal(m_prior, C_M, size=1000)

with _lock:
    fig, ax = plt.subplots(1,3, figsize=(10,4))
    for i in range(len(m_true)):
        _,_,l1 = ax[i].hist(prior_dist[:,i], bins=40, alpha=0.3, label="Prior", color="k")
        _,_,l2 = ax[i].hist(post_dist[:,i], bins=40, alpha=0.6, color='tab:red', label="Posterior")
        l3 = ax[i].axvline(m_true[i], c="k", linewidth="2", label="True mean")
        ax[i].set_title(f"Parameter $m_{i+1}$")
        ax[i].axes.yaxis.set_visible(False)
    fig.subplots_adjust(bottom=0.3, wspace=0.33)
    ax[1].legend(handles=[l1[0], l2[0], l3], loc='upper center', bbox_to_anchor=(0.5, -0.2), shadow=False, ncol=3)
    st.pyplot(fig)

st.markdown(r"""
## Reconstructing Data
The posterior we have derived is the set of three means, with the covariance matrix corresponding to these. Now, we want to plot these in *data space*, that is, we want to see what these parameters produce after putting them through the original projectile motion model. The results are shown below. The prior mean might look far off everything else; but this makes sense: the purpose of the prior was only to give the model a *starting place* in a sense.

The credible region is simply the area in which 95% of the probability falls. This is similar to a confidence interval; however the confidence interval is a frequentist concept whereas the credible interval is a Bayesian concept. If you change the parameters in the sidebar you'll see how this credible interval shrinks or expands. Ideally we want it to be as tight as possible.
""")

with _lock:
    fig, ax = plt.subplots(figsize=(6.50127,3))

    d_map = f(t, m_map) # "pushed forward" posterior mean (pushed forward into data-space that is)
    C_pushed = G @ C_M_p @ G.T # "pushed forward" posterior covariance matrix

    l1, = ax.plot(t, d ,'*', label='Data $\mathbf{d}$', c='k', markersize=2)
    l2, = ax.plot(t, f(t, m_true), label="True data space mean $\mathbf{Gm}_{true}$", c="tab:orange")
    l3, = ax.plot(t, f(t, m_prior), label="Prior data space mean $\mathbf{Gm}_{prior}$")
    l4, = ax.plot(t, d_map, label="Posterior data space mean $\mathbf{Gm}_{post}$",c="k");
    ax.plot(t, d_map + 1.96*np.sqrt(np.diag(C_pushed)), ":", c="k")
    l5, = ax.plot(t, d_map - 1.96*np.sqrt(np.diag(C_pushed)), ":", c="k", label="95% credible region")
    # ax.set_title("Data space solution: compare with least squares version!")
    ax.set_xlabel("Time")
    ax.set_ylabel("Height")

    fig.subplots_adjust(bottom=0.3, wspace=0.33)
    ax.legend(handles=[l1, l2, l3, l4, l5], loc='upper center', 
        bbox_to_anchor=(0.5, -0.25), shadow=False)

    st.pyplot(fig)
