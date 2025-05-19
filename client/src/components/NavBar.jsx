import axios from '../api/axios';
import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Navbar, Nav, Button, Container } from 'react-bootstrap';
import { useNavigate, useLocation } from 'react-router-dom';

const NavBar = ({ product, setProduct }) => {
    const navigate = useNavigate();
    const location = useLocation();
    const [activeButton, setActiveButton] = useState(null);
    const [shoesRevenue, setShoesRevenue] = useState(null);
    const [clothingRevenue, setClothingRevenue] = useState(null);
    const [accessoriesRevenue, setAccessoriesRevenue] = useState(null);
    const [lastRefreshed, setLastRefreshed] = useState(new Date().toLocaleString());

    const navigateTo = (path) => {
        navigate(path);
    };

    useEffect(() => {
        const fetchRevenues = async () => {
            try {
                const shoesResponse = await axios.get('/get_shoe_sale');
                setShoesRevenue(shoesResponse.data.total_revenue);

                const clothingResponse = await axios.get('/get_clothing_sale');
                setClothingRevenue(clothingResponse.data.total_revenue);

                const accessoriesResponse = await axios.get('/get_accessory_sale');
                setAccessoriesRevenue(accessoriesResponse.data.total_revenue);
            } catch (error) {
                console.error('Error fetching revenues:', error);
            }
        };

        fetchRevenues();

        if (!product) {
            setActiveButton('Shoe');
            setProduct('Shoe');
        } else {
            setActiveButton(product);
        }

        const intervalId = setInterval(() => {
            fetchRevenues();
            setLastRefreshed(new Date().toLocaleString());
        }, 60000);

        return () => clearInterval(intervalId);
    }, [product, setProduct]);

    const handleButtonClick = (buttonName) => {
        setActiveButton(buttonName);
        setProduct(buttonName);
    };

    const getButtonStyle = (buttonName) => {        
        return {
            backgroundColor: buttonName === 'Shoe' ? '#ff7f7f' : buttonName === 'Clothing' ? '#90ee90' : '#87cefa',
            borderColor: activeButton === 'Shoe' && buttonName === 'Shoe' ? 'red' : activeButton === 'Clothing' && buttonName === 'Clothing' ? 'green' : activeButton === 'Accessory' && buttonName === 'Accessory' ? 'blue' : 'transparent',
            borderWidth: '4px',
            transform: activeButton === buttonName ? 'scale(1.2)' : 'scale(1)',
            transition: 'transform 0.2s'
        };
    };

    return (
        <>
        <Navbar expand="lg" className="flex-column" style={{ backgroundColor: '#f8f9fa' }}>
            <Container className="d-flex justify-content-between align-items-center">
                <Nav className="me-auto">
                    <Navbar.Text style={{ fontWeight: 'bold', fontSize: '1.5rem' }}>Product Tracker</Navbar.Text>
                </Nav>
                <Nav className="mx-auto" style={{ position: 'absolute', left: '50%', transform: 'translateX(-50%)' }}>
                    <Button 
                        variant="outline-secondary" 
                        className="mx-2" 
                        style={{ backgroundColor: location.pathname === '/dashboard' ? 'orange' : 'transparent' }} 
                        onClick={() => navigateTo('/dashboard')}
                    >
                        Dashboard
                    </Button>
                    <Button 
                        variant="outline-secondary" 
                        className="mx-2" 
                        style={{ backgroundColor: location.pathname === '/product-list' ? 'orange' : 'transparent' }} 
                        onClick={() => navigateTo('/product-list')}
                    >
                        Product List
                    </Button>
                    <Button 
                        variant="outline-secondary" 
                        className="mx-2" 
                        style={{ backgroundColor: location.pathname === '/order' ? 'orange' : 'transparent' }} 
                        onClick={() => navigateTo('/order')}
                    >
                        Order
                    </Button>
                </Nav>
                <Button variant="outline-danger">Quit</Button>
            </Container>
        </Navbar>
        {location.pathname !== '/order' && (
            <Container className="d-flex justify-content-around mt-3" style={{ paddingBottom: '20px' }}>
                <Button 
                    variant="primary" 
                    className="flex-fill mx-4" 
                    style={getButtonStyle('Shoe')} 
                    onClick={() => handleButtonClick('Shoe')}
                >
                    <div style={{ fontSize: '1.2rem' }}>Shoe</div>
                    <div>Total Revenue: {shoesRevenue !== null && `$ ${shoesRevenue}`}</div>
                </Button>
                <Button 
                    variant="primary" 
                    className="flex-fill mx-4" 
                    style={getButtonStyle('Clothing')} 
                    onClick={() => handleButtonClick('Clothing')}
                >
                    <div style={{ fontSize: '1.2rem' }}>Clothing</div>
                    <div>Total Revenue: {clothingRevenue !== null && `$ ${clothingRevenue}`}</div>
                </Button>
                <Button 
                    variant="primary" 
                    className="flex-fill mx-4" 
                    style={getButtonStyle('Accessory')} 
                    onClick={() => handleButtonClick('Accessory')}
                >
                    <div style={{ fontSize: '1.2rem' }}>Accessory</div>
                    <div>Total Revenue: {accessoriesRevenue !== null && `$ ${accessoriesRevenue}`}</div>
                </Button>
            </Container>
        )}
        <Container className="d-flex justify-content-center mt-3">
            <div>Last refreshed: {lastRefreshed}</div>
        </Container>
        </>
    );
};

export default NavBar;
