import axios from '../api/axios';
import React, { useEffect, useState } from 'react';
import { Pie, Line, Bar, Bubble } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, LineElement, BarElement, CategoryScale, LinearScale, PointElement, Title, Tooltip, Legend } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col } from 'react-bootstrap';

ChartJS.register(ArcElement, LineElement, BarElement, CategoryScale, LinearScale, PointElement, Title, Tooltip, Legend, ChartDataLabels);

export default function Home({ product, setProduct }) {
    const [productData, setProductData] = useState([]);

    useEffect(() => {
        const fetchData = () => {
            axios.get(`/get_${product.toLowerCase()}`)
                .then(response => {
                    setProductData(response.data);
                })
                .catch(error => {
                    console.error('There was an error fetching the product data!', error);
                });
        };

        fetchData();
        const intervalId = setInterval(fetchData, 60000); // Refresh data every minute

        return () => clearInterval(intervalId); // Cleanup interval on component unmount
    }, [product]);

    const getChartData = (products) => {
        const years = [...new Set(products.map(pd => pd.year))].sort((a, b) => a - b);
        const salesByYear = years.map(year => products.filter(pd => pd.year === year && pd.sold).length);

        const genders = [...new Set(products.map(pd => pd.gender))];
        const genderCounts = genders.map(gender => products.filter(pd => pd.gender === gender).length);

        const types = [...new Set(products.map(pd => pd.type))];
        const totalProducts = products.length;
        const typeCounts = types.map(type => products.filter(pd => pd.type === type).length);
        const typePercentages = typeCounts.map(count => ((count / totalProducts) * 100).toFixed(2));

        const bubbleData = products.map(pd => ({
            x: pd.factory_cost,
            y: pd.retail_price - pd.factory_cost,
            r: ((pd.retail_price / pd.factory_cost) * 5).toFixed(2) // Adjust the size as needed
        }));

        return {
            lineData: {
                labels: years,
                datasets: [{
                    label: `${product} Sold by Year`,
                    data: salesByYear,
                    fill: false,
                    backgroundColor: ['#36A2EB'],
                    borderColor: '#36A2EB'
                }]
            },
            barData: {
                labels: genders,
                datasets: [{
                    label: `${product} Distribution by Gender`,
                    data: genderCounts,
                    backgroundColor: ['#4BC0C0', '#9966FF', '#FF9F40']
                }]
            },
            pieData: {
                labels: types,
                datasets: [{
                    data: typePercentages,
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40']
                }]
            },
            bubbleData: {
                datasets: [{
                    label: 'Cost vs Profit vs Success Rate',
                    data: bubbleData,
                    backgroundColor: '#FF6384'
                }]
            }
        };
    };

    const { pieData, lineData, barData, bubbleData } = getChartData(productData);

    return (
        <Container className="d-flex flex-column align-items-center" style={{ maxWidth: '75%'}}>
            <Row className="my-4 w-100 justify-content-center">
                <Col md={6}>
                    <h2>Number of {product} by Gender</h2>
                    <Bar data={barData} />
                </Col>
                <Col md={6}>
                    <h2>{product} Sold by Year</h2>
                    <Line data={lineData} />
                </Col>
            </Row>
            <Row className="mb-5 w-100 justify-content-center">
                <Col md={6} style={{ height: '30vw' }}>
                    <h2>{product} Types Distribution</h2>
                    <Pie data={pieData} />
                </Col>
                <Col md={6}>
                    <h2>Cost vs Profit vs Success Rate</h2>
                    <Bubble data={bubbleData} />
                </Col>
            </Row>
        </Container>
    );
}
