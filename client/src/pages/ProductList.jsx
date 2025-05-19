import axios from '../api/axios';
import React, { useEffect, useState } from 'react';
import { Chart as ChartJS, ArcElement, LineElement, BarElement, CategoryScale, LinearScale, PointElement, Title, Tooltip, Legend } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container, Row, Col, Form, Button, Modal } from 'react-bootstrap';

ChartJS.register(ArcElement, LineElement, BarElement, CategoryScale, LinearScale, PointElement, Title, Tooltip, Legend, ChartDataLabels);

export default function Home({ product, setProduct }) {
    const [productData, setProductData] = useState([]);
    const [editRowId, setEditRowId] = useState(null);
    const [editFormData, setEditFormData] = useState({});

    const [activeButton, setActiveButton] = useState(null);
    const [shoesRevenue, setShoesRevenue] = useState(null);
    const [clothingRevenue, setClothingRevenue] = useState(null);
    const [accessoriesRevenue, setAccessoriesRevenue] = useState(null);

    const [showModal, setShowModal] = useState(false);
    const [newProductData, setNewProductData] = useState({
        name: '',
        type: '',
        age_group: '',
        gender: '',
        year: '',
        retail_price: '',
        factory_cost: '',
        target_cost: '',
        sold: ''
    });

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
    }, []);

    useEffect(() => {
        axios.get(`/get_${product.toLowerCase()}`)
            .then(response => {
                setProductData(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the product data!', error);
            });
    }, [product]);
    
    const handleShowModal = () => setShowModal(true);
    const handleCloseModal = () => setShowModal(false);
    
    const handleNewProductChange = (event) => {
        const { name, value } = event.target;
        setNewProductData({ ...newProductData, [name]: value });
    };
    
    const handleNewProductSubmit = (event) => {
        event.preventDefault();
        axios.post(`/add_${product.toLowerCase()}`, newProductData)
            .then(response => {
                setProductData([...productData, response.data]);
                setShowModal(false);
                setNewProductData({
                    name: '',
                    type: '',
                    age_group: '',
                    gender: '',
                    year: '',
                    retail_price: '',
                    factory_cost: '',
                    target_cost: '',
                    sold: ''
                });
            })
            .catch(error => {
                console.error('There was an error adding the product data!', error);
            });
    };

    const handleEditClick = (event, pd) => {
        event.preventDefault();
        setEditRowId(pd.id);
        setEditFormData({ ...pd });
    };

    const handleEditFormChange = (event) => {
        const { name, value } = event.target;
        setEditFormData({ ...editFormData, [name]: value });
    };

    const handleEditFormSubmit = (event) => {
        event.preventDefault();
        axios.put(`/update_${product.toLowerCase()}/${editRowId}`, editFormData)
            .then(response => {
                const updatedProductData = productData.map(pd => (pd.id === editRowId ? editFormData : pd));
                setProductData(updatedProductData);
                setEditRowId(null);
            })
            .catch(error => {
                console.error('There was an error updating the product data!', error);
            });
    };

    const handleDeleteClick = (productId) => {
        if (window.confirm('Are you sure you want to delete this product?')) {
            axios.delete(`/delete_${product.toLowerCase()}/${productId}`)
                .then(() => {
                    setProductData(productData.filter(pd => pd.id !== productId));
                })
                .catch(error => {
                    console.error('There was an error deleting the product!', error);
                });
        }
    };

    return (
        <>
            <Container className="d-flex flex-column align-items-center" style={{ maxWidth: '90%' }}>
                <Row className="my-4 w-100">
                    <Col>
                        <div className="d-flex justify-content-between align-items-center">
                            <h3>{product} Information</h3>
                            <Button className="btn btn-success btn-sm" onClick={handleShowModal}>+ Add</Button>
                        </div>
                        <div style={{ maxHeight: '500px', overflowY: 'auto' }}>
                            <form onSubmit={handleEditFormSubmit}>
                                <table className="table table-striped">
                                    <thead style={{ position: 'sticky', top: 0, backgroundColor: 'white', zIndex: 1 }}>
                                        <tr>
                                            <th>ID</th>
                                            <th>Name</th>
                                            <th>Type</th>
                                            <th>Age Group</th>
                                            <th>Gender</th>
                                            <th>Year</th>
                                            <th>Retail Price</th>
                                            <th>Factory Cost</th>
                                            <th>Target Cost</th>
                                            <th>Sold</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {productData.map(pd => (
                                            editRowId === pd.id ? (
                                                <tr key={pd.id}>
                                                    <td>{pd.id}</td>
                                                    <td><Form.Control type="text" name="name" value={editFormData.name} onChange={handleEditFormChange} /></td>
                                                    <td><Form.Control type="text" name="type" value={editFormData.type} onChange={handleEditFormChange} /></td>
                                                    <td><Form.Control type="text" name="age_group" value={editFormData.age_group} onChange={handleEditFormChange} /></td>
                                                    <td><Form.Control type="text" name="gender" value={editFormData.gender} onChange={handleEditFormChange} /></td>
                                                    <td><Form.Control type="text" name="year" value={editFormData.year} onChange={handleEditFormChange} /></td>
                                                    <td><Form.Control type="text" name="retail_price" value={editFormData.retail_price} onChange={handleEditFormChange} /></td>
                                                    <td><Form.Control type="text" name="factory_cost" value={editFormData.factory_cost} onChange={handleEditFormChange} /></td>
                                                    <td><Form.Control type="text" name="target_cost" value={editFormData.target_cost} onChange={handleEditFormChange} /></td>
                                                    <td><Form.Control type="text" name="sold" value={editFormData.sold} onChange={handleEditFormChange} /></td>
                                                    <td>
                                                        <Button type="submit" className="btn btn-primary btn-sm me-2">💾</Button>
                                                        <Button onClick={() => setEditRowId(null)} className="btn btn-secondary btn-sm">❌</Button>
                                                    </td>
                                                </tr>
                                            ) : (
                                                <tr key={pd.id}>
                                                    <td>{pd.id}</td>
                                                    <td>{pd.name}</td>
                                                    <td>{pd.type}</td>
                                                    <td>{pd.age_group}</td>
                                                    <td>{pd.gender}</td>
                                                    <td>{pd.year}</td>
                                                    <td>{pd.retail_price}</td>
                                                    <td>{pd.factory_cost}</td>
                                                    <td>{pd.target_cost}</td>
                                                    <td>{pd.sold}</td>
                                                    <td>
                                                        <button className="btn btn-primary btn-sm me-2" onClick={(event) => handleEditClick(event, pd)}>✏️</button>
                                                        <button className="btn btn-danger btn-sm" onClick={() => handleDeleteClick(pd.id)}>🗑️</button>
                                                    </td>
                                                </tr>
                                            )
                                        ))}
                                    </tbody>
                                </table>
                            </form>
                        </div>
                    </Col>
                </Row>
            </Container>
    
            <Modal show={showModal} onHide={handleCloseModal}>
                <Modal.Header closeButton>
                    <Modal.Title>Add New Product</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form onSubmit={handleNewProductSubmit}>
                        <Row>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Name</Form.Label>
                                    <Form.Control type="text" name="name" value={newProductData.name} onChange={handleNewProductChange} />
                                </Form.Group>
                            </Col>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Type</Form.Label>
                                    <Form.Control type="text" name="type" value={newProductData.type} onChange={handleNewProductChange} />
                                </Form.Group>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Age Group</Form.Label>
                                    <Form.Control type="text" name="age_group" value={newProductData.age_group} onChange={handleNewProductChange} />
                                </Form.Group>
                            </Col>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Gender</Form.Label>
                                    <Form.Control type="text" name="gender" value={newProductData.gender} onChange={handleNewProductChange} />
                                </Form.Group>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Year</Form.Label>
                                    <Form.Control type="text" name="year" value={newProductData.year} onChange={handleNewProductChange} />
                                </Form.Group>
                            </Col>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Retail Price</Form.Label>
                                    <Form.Control type="text" name="retail_price" value={newProductData.retail_price} onChange={handleNewProductChange} />
                                </Form.Group>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Factory Cost</Form.Label>
                                    <Form.Control type="text" name="factory_cost" value={newProductData.factory_cost} onChange={handleNewProductChange} />
                                </Form.Group>
                            </Col>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Target Cost</Form.Label>
                                    <Form.Control type="text" name="target_cost" value={newProductData.target_cost} onChange={handleNewProductChange} />
                                </Form.Group>
                            </Col>
                        </Row>
                        <Form.Group className="mb-3">
                            <Form.Label>Sold</Form.Label>
                            <Form.Control type="text" name="sold" value={newProductData.sold} onChange={handleNewProductChange} />
                        </Form.Group>
                        <Button variant="primary" type="submit">
                            Add Product
                        </Button>
                    </Form>
                </Modal.Body>
            </Modal>
        </>
    );
}
