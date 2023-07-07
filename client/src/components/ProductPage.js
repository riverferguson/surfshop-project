import React from 'react'
import ProductCard from './ProductCard'

const ProductPage = ({products}) => {
const mappedProducts = products.map(product => <ProductCard key={product.id} product={product}/>)

  return (
    <div>{mappedProducts}</div>
  )
}

export default ProductPage