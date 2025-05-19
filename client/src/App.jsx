import { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Dashboard from './pages/Dashboard';
import ProductList from './pages/ProductList';
import Order from './pages/Order';
import NavBar from './components/NavBar';

export default function App() {
  const [product, setProduct] = useState(localStorage.getItem('product') || 'Shoes');

  return (
    <BrowserRouter>
      <NavBar product={product} setProduct={setProduct}/>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" />} />
        <Route path="/dashboard" element={<Dashboard product={product} setProduct={setProduct}/>} />
        <Route path="/product-list" element={<ProductList product={product} setProduct={setProduct}/>} />
        <Route path="/order" element={<Order />} />
      </Routes>
    </BrowserRouter>
  );
}
