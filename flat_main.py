import pandas as pd
import time
import warnings

warnings.filterwarnings("ignore")

from flat_function import get_my_flat

flatDf = pd.read_excel('flat_pattern.xlsx')
links = list(flatDf.loc[pd.isna(flatDf['Метро'])]['Ссылка'])

success = 0
fails = 0

for i in range(len(links)):
    print('Ссылка: ' + str(links[i]))

    parserError = ""
    try:
        resultSet = get_my_flat(links[i])
    except Exception as e:
        parserError = str(e)

    if parserError == "":
        print(pd.DataFrame.from_dict(resultSet, orient='index'))
        print('\n')
        success += 1

        flatDf.loc[flatDf['Ссылка'] == links[i], 'Метро'] = resultSet['Все станции: ']
        flatDf.loc[flatDf['Ссылка'] == links[i], 'Ближайшая станция метро'] = resultSet['Ближайшее метро: ']
        flatDf.loc[flatDf['Ссылка'] == links[i], 'Удаленность от метро (мин)'] = resultSet['Удаленность от метро (мин): ']
        flatDf.loc[flatDf['Ссылка'] == links[i], 'Площадь (м2)'] = resultSet['Площадь (м2): ']
        flatDf.loc[flatDf['Ссылка'] == links[i], 'Посудомойка'] = resultSet['Посудомойка: ']
        flatDf.loc[flatDf['Ссылка'] == links[i], 'Стоимость'] = resultSet['Стоимость: ']
        flatDf.loc[flatDf['Ссылка'] == links[i], 'Комиссия %'] = resultSet['Комиссия %']
    else:
        fails += 1
        print('Влетел в ошибку!')
        print(parserError)
        print('\n')
        flatDf.loc[flatDf['Ссылка'] == links[i], 'Ошибка парсера'] = parserError
    time.sleep(2)

flatDf.to_excel('flat_pattern_filled_1.xlsx')
print('\n\nFINISHED')
print('Success: ' + str(success))
print('Fails: ' + str(fails))
