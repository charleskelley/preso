# preso

**preso** is a Python package for creating static and dynamic visualizations
that can be easily incorporated into presentations using a user defined theme.

Most presentations end up using the same types of plots but depending on the
presentation medium (i.e. HTML, Power Point, etc...), the format of the plot
needs to be appropriately customized and different Python core visualization
packages excel at dfferent formats. For example, Matplotlib and Seaborn are
particularly good for creating visualizations for static medium, while Plotly
is fantastic for dynamic presentation in HTML settings. Additionally, most
companies have specific templates, branding guidelines, and color palettes for
presentations.

The preso package addresses these issues, making it easy to create high quality
visualizations fit for presentation using a user defined theme that meets
a given companies branding.

The goal is to use existing Matplotlib, Seaborn, and Plotly/Plotly Express
package methods with customized styling as much as possible, and to align API
differences between the packages to use a standardized function argument
convention by providing a wrapper API that is consistent no matter which
plotting engine is used under the hood.

## Static plots

Static plots and features are created using Seaborn methods first and then
augmented with or created with Matplotlib methods when it's too difficult or
impossible to achieve the desired aesthetic.

## Dynamic plots

Dynamic plots and features are created using Plotly Express methods first and
then augmented with or created with Plotly Graph Object methods when it's too
difficult or impossible to achieve the desired aesthetic.

