import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Upload and clean up df
contraceptive = pd.read_csv(r'C:\Users\jroef\Downloads\contraceptive.csv')
contraceptive_df = contraceptive[~(contraceptive['Region, subregion and country'] == '  Western Africa')]

#Create columns for relative percentage of women avoiding pregnancy
contraceptive_df['Avoiding Pregnancy'] = 100-contraceptive_df['Not wanting to avoid pregnancy*']
contraceptive_df['Percent of avoiding using modern'] = round(contraceptive_df['Met need— Using modern methods']/contraceptive_df['Avoiding Pregnancy']*100,2)
contraceptive_df['Percent of avoiding using trad'] = round(contraceptive_df['Using traditional methods']/contraceptive_df['Avoiding Pregnancy']*100,2)
contraceptive_df['Percent of avoiding not using'] = round(contraceptive_df['Using no method']/contraceptive_df['Avoiding Pregnancy']*100,2)
contraceptive_df['total perc'] = contraceptive_df['Percent of avoiding using modern'] + contraceptive_df['Percent of avoiding using trad'] + contraceptive_df['Percent of avoiding not using']
contraceptive_df['offset'] = (contraceptive_df['total perc'] - 100)/3

#Round off numbers to add to 100
contraceptive_df['Percent of avoiding using modern'] = round(contraceptive_df['Percent of avoiding using modern'] - contraceptive_df['offset'],2)
contraceptive_df['Percent of avoiding using trad'] = round(contraceptive_df['Percent of avoiding using trad'] - contraceptive_df['offset'],2)
contraceptive_df['Percent of avoiding not using'] = round(contraceptive_df['Percent of avoiding not using'] - contraceptive_df['offset'],2)

#Create a choropleth graph for a given continent
def get_continent_choro(continent):
    contraceptive_df_SA = contraceptive_df[contraceptive_df[' Continent '] == continent]

    trace = go.Choropleth(
        locations=contraceptive_df_SA['Region, subregion and country'],
        z = contraceptive_df_SA['Avoiding Pregnancy'].astype(float),
        locationmode = 'country names', # set of locations match entries in `locations`
        colorscale = 'ylgn',
        colorbar_title = "% of Women",
        )

    return trace

#Create an avoiding pregnancy bar graph for oceania since graph doesn't show well
def get_continent_avoiding_bar(continent):
    contraceptive_df_SA = contraceptive_df[contraceptive_df[' Continent '] == continent]

    countries_SA = contraceptive_df_SA['Region, subregion and country'].values
    countries_SA = list(map(replace_word, countries_SA))
    countries_SA_avoid = contraceptive_df_SA['Avoiding Pregnancy'].values

    trace = go.Bar(name = 'Country', y=countries_SA, x=countries_SA_avoid, orientation='h', marker_color='#006600')

    return trace

#Add some breaks to country names for better display
def replace_word(x):
    if x == 'French Guiana (g)':
        x = 'French<br>Guiana (g)'
    elif x == 'Rep. of Korea (South)':
        x = 'Rep. of Korea(S)'
    elif x == 'Dem. Rep. of Korea (North)':
        x = 'Dem. Rep. of Korea(N)'
    elif x == 'Fed. St. of Micronesia (d)':
        x = 'Fed. St. of<br>Micronesia (d)'
    elif x == 'Papua New Guinea':
        x = 'Papua<br>New Guinea'
    return x

#Create traces for different methods to combine into a stacked graph in the subplots
def get_region_bar(region):
    contraceptive_df_SA = contraceptive_df[contraceptive_df[' Region '] == region]

    countries_SA = contraceptive_df_SA['Region, subregion and country'].values
    countries_SA = list(map(replace_word, countries_SA))
    countries_SA_modern = contraceptive_df_SA['Percent of avoiding using modern'].values
    countries_SA_trad = contraceptive_df_SA['Percent of avoiding using trad'].values
    countries_SA_no = contraceptive_df_SA['Percent of avoiding not using'].values

    trace1 = go.Bar(name='Modern', y=countries_SA, x=countries_SA_modern, orientation='h', marker_color='#009900')
    trace2 = go.Bar(name='Traditional', y=countries_SA, x=countries_SA_trad, orientation='h', marker_color='#FFFF00')
    trace3 = go.Bar(name='No Methods', y=countries_SA, x=countries_SA_no, orientation='h', marker_color='#990000')

    return trace1,trace2,trace3

#South America
fig_cloro_SA = get_continent_choro('LATIN AMERICA AND THE CARIBBEAN')

fig_bar_car1, fig_bar_car2, fig_bar_car3 = get_region_bar('  Caribbean')
fig_bar_ca1, fig_bar_ca2, fig_bar_ca3 = get_region_bar('  Central America')
fig_bar_so_am1, fig_bar_so_am2, fig_bar_so_am3 = get_region_bar('  South America')

fig_sa = make_subplots(
    rows=2, cols=3,
    column_widths=[0.3, 0.3,0.4],
    row_heights=[0.6, 0.4],
    specs=[[{"type": "bar"}, {"type": "bar", 'rowspan':2}, {"type": "choropleth"}],[{"type": "bar"},  None, {"type": "choropleth"}]],
    subplot_titles=("Caribbean", "South America", "", "Central America", '', ''),
    horizontal_spacing=0.1,
    vertical_spacing=0.15
)

fig_sa.append_trace(fig_bar_car1, 1,1)
fig_sa.append_trace(fig_bar_car2, 1,1)
fig_sa.append_trace(fig_bar_car3, 1,1)
fig_sa.append_trace(fig_cloro_SA, 1,3)
fig_sa.append_trace(fig_bar_ca1, 2,1)
fig_sa.append_trace(fig_bar_ca2, 2,1)
fig_sa.append_trace(fig_bar_ca3, 2,1)
fig_sa.append_trace(fig_cloro_SA, 2,3)
fig_sa.append_trace(fig_bar_so_am1, 1,2)
fig_sa.append_trace(fig_bar_so_am2, 1,2)
fig_sa.append_trace(fig_bar_so_am3, 1,2)


fig_sa.update_layout(barmode='stack')
fig_sa.update_geos(scope='north america', row=1, col=3)
fig_sa.update_geos(scope='south america', visible=False, row=2, col=3)
fig_sa.update_layout(showlegend=False)
fig_sa.update_xaxes(range=[0, 100])
#Hack out the title to show for both parts of the graph
fig_sa.update_layout(title_text="Contraceptive Use By Women (15-49) Who Report Avoiding Pregnancy                                         Percentage of Women Who Report Avoiding Pregnancy")
fig_sa.update_xaxes(title_text="Green - Modern Methods<br>Yellow - Traditional Methods<br>Red - No Methods", title_font_size=14, row=2, col=1)
fig_sa.update_xaxes(dict(tickmode = 'array', tickvals = [0,50,100], ticktext = ['0%', '50%', '100%']), row=1, col=1)
fig_sa.update_xaxes(dict(tickmode = 'array', tickvals = [0,50,100], ticktext = ['0%', '50%', '100%']), row=2, col=1)
fig_sa.update_xaxes(dict(tickmode = 'array', tickvals = [0,50,100], ticktext = ['0%', '50%', '100%']), row=1, col=2)

fig_sa.update_layout(   margin=dict(
        l=100,
        r=100,
        b=50,
        t=100,
        pad=4
    ),)

#Africa
fig_cloro_AF = get_continent_choro('AFRICA')

fig_bar_ea1, fig_bar_ea2, fig_bar_ea3 = get_region_bar('Eastern Africa ')
fig_bar_ma1, fig_bar_ma2, fig_bar_ma3 = get_region_bar('  Middle Africa')
fig_bar_saf1, fig_bar_saf2, fig_bar_saf3 = get_region_bar('  Southern Africa')
fig_bar_wa1, fig_bar_wa2, fig_bar_wa3 = get_region_bar('  Western Africa')
fig_bar_na1, fig_bar_na2, fig_bar_na3 = get_region_bar('  Northern Africa')


fig_af = make_subplots(
    rows=2, cols=3,

    row_heights=[0.7, 0.3],
    specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "choropleth"}],[{"type": "bar"},  {"type": "bar"}, {"type": "bar"}]],
    subplot_titles=("Eastern Africa", "Middle Africa", "", "Western Africa", 'Northern Africa', 'Southern Africa'),
    horizontal_spacing=0.1,
    vertical_spacing=0.15)

fig_af.append_trace(fig_bar_ea1, 1,1)
fig_af.append_trace(fig_bar_ea2, 1,1)
fig_af.append_trace(fig_bar_ea3, 1,1)
fig_af.append_trace(fig_cloro_AF, 1,3)

fig_af.append_trace(fig_bar_ma1, 2,1)
fig_af.append_trace(fig_bar_ma2, 2,1)
fig_af.append_trace(fig_bar_ma3, 2,1)

fig_af.append_trace(fig_bar_wa1, 1,2)
fig_af.append_trace(fig_bar_wa2, 1,2)
fig_af.append_trace(fig_bar_wa3, 1,2)

fig_af.append_trace(fig_bar_na1, 2,2)
fig_af.append_trace(fig_bar_na2, 2,2)
fig_af.append_trace(fig_bar_na3, 2,2)

fig_af.append_trace(fig_bar_saf1, 2,3)
fig_af.append_trace(fig_bar_saf2, 2,3)
fig_af.append_trace(fig_bar_saf3, 2,3)


fig_af.update_layout(barmode='stack')
fig_af.update_geos(scope='africa', row=1, col=3)
fig_af.update_layout(showlegend=False)
fig_af.update_xaxes(range=[0, 100])
fig_af.update_layout(title_text="Contraceptive Use By Women (15-49) Who Report Avoiding Pregnancy                                             Percentage of Women Who Report Avoiding Pregnancy")
fig_af.update_xaxes(title_text="Green - Modern Methods<br>Yellow - Traditional Methods<br>Red - No Methods", title_font_size=14, row=2, col=1)
fig_af.update_xaxes(dict(tickmode = 'array', tickvals = [0,50,100], ticktext = ['0%', '50%', '100%']), row=1, col=1)
fig_af.update_xaxes(dict(tickmode = 'array', tickvals = [0,50,100], ticktext = ['0%', '50%', '100%']), row=2, col=1)
fig_af.update_xaxes(dict(tickmode = 'array', tickvals = [0,50,100], ticktext = ['0%', '50%', '100%']), row=1, col=2)
fig_af.update_layout(   margin=dict(
        l=100,
        r=100,
        b=50,
        t=100,
        pad=4
    ),)

#Asia
fig_cloro_AS = get_continent_choro('ASIA‡')

fig_bar_eas1, fig_bar_eas2, fig_bar_eas3 = get_region_bar('  Eastern Asia ')
fig_bar_cas1, fig_bar_cas2, fig_bar_cas3 = get_region_bar('  Central Asia ')
fig_bar_sas1, fig_bar_sas2, fig_bar_sas3 = get_region_bar('  Southern Asia ')
fig_bar_seas1, fig_bar_seas2, fig_bar_seas3 = get_region_bar('  Southeast Asia ')
fig_bar_was1, fig_bar_was2, fig_bar_was3 = get_region_bar('  Western Asia ')

fig_as = make_subplots(
    rows=2, cols=3,

    row_heights=[0.7, 0.3],
    specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "choropleth"}],[{"type": "bar"},  {"type": "bar"}, {"type": "bar"}]],
    subplot_titles=("Southeast Asia", "Western Asia", "", "Central Asia", 'Southern Asia', 'Eastern Asia'),
    horizontal_spacing=0.12,
    vertical_spacing=0.15)

fig_as.append_trace(fig_bar_eas1, 2,3)
fig_as.append_trace(fig_bar_eas2, 2,3)
fig_as.append_trace(fig_bar_eas3, 2,3)
fig_as.append_trace(fig_cloro_AS, 1,3)

fig_as.append_trace(fig_bar_cas1, 2,1)
fig_as.append_trace(fig_bar_cas2, 2,1)
fig_as.append_trace(fig_bar_cas3, 2,1)

fig_as.append_trace(fig_bar_sas1, 2,2)
fig_as.append_trace(fig_bar_sas2, 2,2)
fig_as.append_trace(fig_bar_sas3, 2,2)

fig_as.append_trace(fig_bar_seas1, 1,1)
fig_as.append_trace(fig_bar_seas2, 1,1)
fig_as.append_trace(fig_bar_seas3, 1,1)

fig_as.append_trace(fig_bar_was1, 1,2)
fig_as.append_trace(fig_bar_was2, 1,2)
fig_as.append_trace(fig_bar_was3, 1,2)


fig_as.update_layout(barmode='stack')
fig_as.update_geos(scope='asia', row=1, col=3)
fig_as.update_layout(showlegend=False)
fig_as.update_xaxes(range=[0, 100])
fig_as.update_layout(title_text="Contraceptive Use By Women (15-49) Who Report Avoiding Pregnancy                                         Percentage of Women Who Report Avoiding Pregnancy")
fig_as.update_xaxes(title_text="Green - Modern Methods<br>Yellow - Traditional Methods<br>Red - No Methods", title_font_size=14, row=2, col=1)
fig_as.update_xaxes(dict(tickmode = 'array', tickvals = [0,50,100], ticktext = ['0%', '50%', '100%']), row=1, col=1)
fig_as.update_xaxes(dict(tickmode = 'array', tickvals = [0,50,100], ticktext = ['0%', '50%', '100%']), row=2, col=1)
fig_as.update_xaxes(dict(tickmode = 'array', tickvals = [0,50,100], ticktext = ['0%', '50%', '100%']), row=1, col=2)
fig_as.update_layout(   margin=dict(
        l=100,
        r=100,
        b=50,
        t=100,
        pad=4
    ),)

#Oceania
fig_bar_OC  = get_continent_avoiding_bar('OCEANIA')


fig_bar_me1, fig_bar_me2, fig_bar_me3 = get_region_bar('  Melanesia')
fig_bar_mi1, fig_bar_mi2, fig_bar_mi3 = get_region_bar('  Micronesia')
fig_bar_po1, fig_bar_po2, fig_bar_po3 = get_region_bar('  Polynesia')

fig_oc = make_subplots(
    rows=2, cols=3,
    column_widths=[0.3, 0.3,0.4],
    row_heights=[0.6, 0.4   ],
    specs=[[{"type": "bar"}, {"type": "bar", 'rowspan':2}, {"type": "bar", 'rowspan':2}],[{"type": "bar"},  None, None]],
    subplot_titles=("Polynesia", "Micronesia", "", "Melanesia", '', ''),
    horizontal_spacing=0.1,
    vertical_spacing=0.1
)

fig_oc.append_trace(fig_bar_po1, 1,1)
fig_oc.append_trace(fig_bar_po2, 1,1)
fig_oc.append_trace(fig_bar_po3, 1,1)

fig_oc.append_trace(fig_bar_OC, 1,3)

fig_oc.append_trace(fig_bar_mi1, 2,1)
fig_oc.append_trace(fig_bar_mi2, 2,1)
fig_oc.append_trace(fig_bar_mi3, 2,1)

fig_oc.append_trace(fig_bar_me1, 1,2)
fig_oc.append_trace(fig_bar_me2, 1,2)
fig_oc.append_trace(fig_bar_me3, 1,2)


fig_oc.update_layout(barmode='stack')
fig_oc.update_layout(showlegend=False)
fig_oc.update_xaxes(range=[0, 100])
fig_oc.update_layout(title_text="Contraceptive Use By Women (15-49) Who Report Avoiding Pregnancy                                         Percentage of Women Who Report Avoiding Pregnancy")
fig_oc.update_xaxes(title_text="Green - Modern Methods<br>Yellow - Traditional Methods<br>Red - No Methods", title_font_size=14, row=2, col=1)
fig_oc.update_xaxes(dict(tickmode = 'array', tickvals = [0,50,100], ticktext = ['0%', '50%', '100%']), row=1, col=1)
fig_oc.update_xaxes(dict(tickmode = 'array', tickvals = [0,50,100], ticktext = ['0%', '50%', '100%']), row=2, col=1)
fig_oc.update_xaxes(dict(tickmode = 'array', tickvals = [0,50,100], ticktext = ['0%', '50%', '100%']), row=1, col=2)
fig_oc.update_xaxes(dict(tickmode = 'array', tickvals = [0,20,40,60,80,100], ticktext = ['0%', '20%', '40%', '60%', '80%', '100%']), row=1, col=3)
fig_oc.update_layout(   margin=dict(
        l=100,
        r=100,
        b=50,
        t=100,
        pad=4
    ),)

fig_oc.show()