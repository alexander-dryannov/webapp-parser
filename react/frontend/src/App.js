import React, { useState } from 'react'
import { useQuery } from '@apollo/client'
import { GET_PRICE_AERODAR, GET_PRICE_AEROSIB, GET_PRICE_ARTIS, GET_PRICE_MDCARGO, GET_PRICE_TRANSCOM } from './graphql/TypeDefs'

import "./App.scss"
import { kaReducer, Table } from 'ka-table';
import { DataType, EditingMode, SortingMode } from 'ka-table/enums';

function Xds(limit) {
  // const { loading, error, data } = useQuery(GET_PRICE_AERODAR)
  // const { loading, error, data } = useQuery(GET_PRICE_ARTIS)
  // const { loading, error, data } = useQuery(GET_PRICE_AEROSIB)
  // const { loading, error, data } = useQuery(GET_PRICE_TRANSCOM)
  const { loading, error, data } = useQuery(GET_PRICE_MDCARGO, {limit: limit})
  console.log("data from XDS", data)
  return [data, loading, error]
}

export default function App() {
  const [data, loading, error] = Xds(2)

  if (loading) {
    console.log("Loading")
  }
  if (error) {
    console.log("Error")
  }
  if (data === undefined) {
    console.log("Нет данных")
  }
  
  const dataArray = data.getPriceAerosib.map(
    (_, price) => (
      {
        column1: price.departure,
        column2: price.appointment,
        column3: price.ak,
        column4: price.cost,
        id: price.id
      }
    )
  );

  const tablePropsInit = {
    columns: [
      { key: 'column1', title: 'departure', dataType: DataType.String },
      { key: 'column2', title: 'appointment', dataType: DataType.String },
      { key: 'column3', title: 'AK', dataType: DataType.String },
      { key: 'column4', title: 'cost', dataType: DataType.String }
    ],
    data: dataArray,
    editingMode: EditingMode.Cell,
    rowKeyField: 'id',
    sortingMode: SortingMode.Single
  };

  const [tableProps, changeTableProps] = useState(tablePropsInit)
  const dispatch = action => {
    changeTableProps(prevState => kaReducer(prevState, action))
  }
  return <Table {...tableProps} dispatch={dispatch} />
}
