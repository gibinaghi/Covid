import wget
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


def df_by_country_sorted_by_date(covid_df, country):
    """función que se queda con un país y ordena los datos según los días"""
    data_by_country = covid_df.loc[covid_df['location'] == country]
    data_by_country_sorted = data_by_country.sort_values('date')
    return data_by_country_sorted


def get_total_cases(data_by_country_sorted):
    """ función que completa los datos faltantes en los casos totales con la media"""
    total_cases = data_by_country_sorted['total_cases'].fillna(data_by_country_sorted['total_cases'].mean())
    return total_cases


def get_total_deaths(data_by_country_sorted):
    """ función que completa los datos faltantes en los muertes totales con la media"""
    total_deaths = data_by_country_sorted['total_deaths'].fillna(data_by_country_sorted['total_deaths'].mean())
    return total_deaths


def covid_plot_one_country(covid_df, country):
    """ función que pinta en un grafico las muertes y casos totales de un país"""
    fig_total_cases = plt.figure()
    data_by_country_sorted = df_by_country_sorted_by_date(covid_df, country)
    date = data_by_country_sorted['date']

    total_cases = get_total_cases(data_by_country_sorted)
    total_deaths = get_total_deaths(data_by_country_sorted)

    plt.plot(date, total_cases, label="Casos totales")
    plt.plot(date, total_deaths, label="Muertes totales")
    plt.xlabel("Fechas")
    plt.title(f'Casos nuevos y muertes por covid en: {country}')
    plt.xlim(0, 300)
    plt.yscale('log')
    plt.show()
    fig_total_cases.savefig('CasosYMuertesTotalesCovidUnPais.png')


def covid_plot_lot_of_countries(covid_df, countries_list, date_init, date_end):
    """ función que pinta en un grafico los casos totales de n paises
    y en otro grafico pinta las muertes totales de n paises"""
    fig_total_cases = plt.figure()
    for country in countries_list:
        data_by_country_sorted = df_by_country_sorted_by_date(covid_df, country)

        date_filter = (data_by_country_sorted['date'] > date_init) & (data_by_country_sorted['date'] <= date_end)
        filtered_df = data_by_country_sorted.loc[date_filter]
        date = filtered_df['date']

        total_cases = get_total_cases(filtered_df).fillna(0)

        plt.xlabel("Fechas")
        plt.plot(date, total_cases, label=country)

    plt.title(f'Casos totales de covid en: {countries_list}')
    plt.legend()
    plt.ylabel("Casos Totales")
    plt.yscale('log')
    plt.show()
    fig_total_cases.savefig('CasosTotalesCovid.png')

    fig_total_deaths = plt.figure()
    for country in countries_list:
        data_by_country_sorted = df_by_country_sorted_by_date(covid_df, country)

        date_filter = (data_by_country_sorted['date'] > date_init) & (data_by_country_sorted['date'] <= date_end)
        filtered_df = data_by_country_sorted.loc[date_filter]
        date = filtered_df['date']

        total_deaths = get_total_deaths(filtered_df).fillna(0)

        plt.xlabel("Fechas")
        plt.plot(date, total_deaths, label=country)

    plt.title(f'Muertes totales de covid en: {countries_list}')
    plt.legend()
    plt.ylabel("Muertes Totales")
    plt.yscale('log')
    plt.show()
    fig_total_deaths.savefig('MuertesTotalesCovid.png')

def covid_plot_two_countries(covid_df, countries_list, date_init, date_end):
    """ función que pinta en un grafico los casos totales de dos paises y marca sus intersecciones,
    luego en otro grafico pinta las muertes totales de dos paises y marca sus intersecciones"""
    fig_total_cases = plt.figure()

    # punto de cruce de casos tortales de dos países
    x = []
    y = []
    df_first_country = df_by_country_sorted_by_date(covid_df, countries_list[0])
    df_second_country = df_by_country_sorted_by_date(covid_df, countries_list[1])
    cx = [df_first_country["date"].iloc[0]]
    cy = [df_first_country["total_cases"].iloc[0]]
    dx = [df_second_country["date"].iloc[0]]
    dy = [df_second_country["total_cases"].iloc[0]]


    for i in range(1, len(df_first_country["date"])):
        cx.append(df_first_country["date"].iloc[i])
        cy.append(df_first_country["total_cases"].iloc[i])
        dx.append(df_second_country["date"].iloc[i])
        dy.append(df_second_country["total_cases"].iloc[i])

        if (dy[i] == cy[i]) or (dy[i] > cy[i] and dy[i - 1] < cy[i - 1]) or (dy[i] < cy[i] and dy[i - 1] > cy[i - 1]):
            x.append(cx[i])
            y.append(cy[i])


    for country in countries_list:
        data_by_country_sorted = df_by_country_sorted_by_date(covid_df, country)

        date_filter = (data_by_country_sorted['date'] > date_init) & (data_by_country_sorted['date'] <= date_end)
        filtered_df = data_by_country_sorted.loc[date_filter]

        date = filtered_df['date']

        total_cases = get_total_cases(filtered_df).fillna(0)

        plt.xlabel("Fechas")
        plt.plot(date, total_cases, label=country)


    plt.subplot(1, 2, 1)
    plt.plot(x, y, 'k.')
    plt.title(f'Casos totales de covid en: {countries_list}')
    plt.legend()
    plt.ylabel("Casos Totales")
    plt.yscale('log')
    plt.show()
    fig_total_cases.savefig('CasosTotalesCovidDosPaises.png')

    fig_total_deaths = plt.figure()
    # punto de cruce de muertes tortales de dos países
    x = []
    y = []
    df_first_country = df_by_country_sorted_by_date(covid_df, countries_list[0])
    df_second_country = df_by_country_sorted_by_date(covid_df, countries_list[1])
    cx = [df_first_country["date"].iloc[0]]
    cy = [df_first_country["total_deaths"].iloc[0]]
    dx = [df_second_country["date"].iloc[0]]
    dy = [df_second_country["total_deaths"].iloc[0]]

    for i in range(1, len(df_first_country["date"])):
        cx.append(df_first_country["date"].iloc[i])
        cy.append(df_first_country["total_deaths"].iloc[i])
        dx.append(df_second_country["date"].iloc[i])
        dy.append(df_second_country["total_deaths"].iloc[i])

        if (dy[i] == cy[i]) or (dy[i] > cy[i] and dy[i - 1] < cy[i - 1]) or (dy[i] < cy[i] and dy[i - 1] > cy[i - 1]):
            x.append(cx[i])
            y.append(cy[i])

    for country in countries_list:
        data_by_country_sorted = df_by_country_sorted_by_date(covid_df, country)

        date_filter = (data_by_country_sorted['date'] > date_init) & (data_by_country_sorted['date'] <= date_end)
        filtered_df = data_by_country_sorted.loc[date_filter]
        date = filtered_df['date']

        total_deaths = get_total_deaths(filtered_df).fillna(0)

        plt.xlabel("Fechas")
        plt.plot(date, total_deaths, label=country)

    plt.subplot(1, 2, 2)
    plt.title(f'Muertes totales de covid en: {countries_list}')
    plt.legend()
    plt.ylabel("Muertes Totales")
    plt.yscale('log')
    plt.show()
    fig_total_deaths.savefig('MuertesTotalesCovidDosPaises.png')


if __name__ == '__main__':
    if not os.path.exists('full_data.csv') or os.stat('full_data.csv').st_size == 0:
        url = 'https://covid.ourworldindata.org/data/ecdc/full_data.csv'
        filename = wget.download(url)

    covid_df = pd.read_csv("full_data.csv")

    countries = input("Ingrese los paises separados por comas: ")
    countries_list = countries.split(",")

    date_init = input("Ingrese la fecha de inicio (formato YYYY-MM-DD): ")
    date_end = input("Ingrese la fecha de fin (formato YYYY-MM-DD): ")

    if len(countries_list) == 1:
        country = countries_list[0]
        covid_plot_one_country(covid_df, country)
    elif len(countries_list) == 2:
        covid_plot_two_countries(covid_df, countries_list, date_init, date_end)
    else:
        covid_plot_lot_of_countries(covid_df, countries_list, date_init, date_end)