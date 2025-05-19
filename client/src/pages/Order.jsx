import React, { useEffect, useState } from 'react';
import axios from '../api/axios';
import { Table, Container, Button, Row, Col, Form, Modal } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const Order = () => {
    const [orders, setOrders] = useState([]);
    const [editRowId, setEditRowId] = useState(null);
    const [editFormData, setEditFormData] = useState({
        order_id: '',
        merchandiser_id: '',
        product_id: '',
        quantity: '',
        order_date: '',
        status: '',
        total_cost: ''
    });

    const [showModal, setShowModal] = useState(false);
    const [newOrderData, setNewOrderData] = useState({
        merchandiser_id: '',
        product_id: '',
        quantity: '',
        order_date: '',
        status: '',
        total_cost: ''
    });

    useEffect(() => {
        axios.get('/get_orders')
            .then(response => {
                setOrders(response.data);
            })
            .catch(error => {
                console.error('There was an error fetching the orders!', error);
            });
    }, []);

    const handleEditFormChange = (event) => {
        const { name, value } = event.target;
        setEditFormData({ ...editFormData, [name]: value });
    };

    const handleEditFormSubmit = (event) => {
        event.preventDefault();
        axios.put(`/update_order/${editRowId}`, editFormData, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                const updatedOrders = orders.map(order => 
                    order.order_id === editRowId ? { ...order, ...editFormData } : order
                );
                setOrders(updatedOrders);
                setEditRowId(null);
            })
            .catch(error => {
                console.error('There was an error updating the order!', error);
            });
    };

    const handleEditClick = (event, order) => {
        event.preventDefault();
        setEditRowId(order.order_id);
        setEditFormData(order);
    };

    const handleShowModal = () => setShowModal(true);
    const handleCloseModal = () => setShowModal(false);

    const handleNewOrderChange = (event) => {
        const { name, value } = event.target;
        setNewOrderData({ ...newOrderData, [name]: value });
    };

    const handleNewOrderSubmit = (event) => {
        event.preventDefault();
        axios.post('/add_order', newOrderData, {
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => {
                setOrders([...orders, response.data]);
                setShowModal(false);
                setNewOrderData({
                    merchandiser_id: '',
                    product_id: '',
                    quantity: '',
                    order_date: '',
                    status: '',
                    total_cost: ''
                });
            })
            .catch(error => {
                console.error('There was an error adding the order!', error);
            });
    };

    const handleDeleteClick = (orderId) => {
        if (window.confirm('Are you sure you want to delete this order?')) {
            axios.delete(`/delete_order/${orderId}`)
                .then(() => {
                    setOrders(orders.filter(order => order.order_id !== orderId));
                })
                .catch(error => {
                    console.error('There was an error deleting the order!', error);
                });
        }
    };

    return (
        <Container className="d-flex flex-column align-items-center" style={{ maxWidth: '90%' }}>
            <Row className="my-4 w-100">
                <Col>
                    <div className="d-flex justify-content-between align-items-center">
                        <h3>Order List</h3>
                        <Button className="btn btn-success btn-sm" onClick={handleShowModal}>+ Add</Button>
                    </div>
                    <div style={{ maxHeight: '600px', overflowY: 'auto' }}>
                        <form onSubmit={handleEditFormSubmit}>
                            <Table striped bordered hover>
                                <thead style={{ position: 'sticky', top: 0, backgroundColor: 'white', zIndex: 1 }}>
                                    <tr>
                                        <th>Order ID</th>
                                        <th>Merchandiser ID</th>
                                        <th>Product ID</th>
                                        <th>Quantity</th>
                                        <th>Order Date</th>
                                        <th>Status</th>
                                        <th>Total Cost</th>
                                        <th>Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {orders.map(order => (
                                        editRowId === order.order_id ? (
                                            <tr key={order.order_id}>
                                                <td>{order.order_id}</td>
                                                <td><Form.Control type="text" name="merchandiser_id" value={editFormData.merchandiser_id} onChange={handleEditFormChange} /></td>
                                                <td><Form.Control type="text" name="product_id" value={editFormData.product_id} onChange={handleEditFormChange} /></td>
                                                <td><Form.Control type="text" name="quantity" value={editFormData.quantity} onChange={handleEditFormChange} /></td>
                                                <td><Form.Control type="text" name="order_date" value={editFormData.order_date} onChange={handleEditFormChange} /></td>
                                                <td><Form.Control type="text" name="status" value={editFormData.status} onChange={handleEditFormChange} /></td>
                                                <td><Form.Control type="text" name="total_cost" value={editFormData.total_cost} onChange={handleEditFormChange} /></td>
                                                <td>
                                                    <Button type="submit" className="btn btn-primary btn-sm me-2">💾</Button>
                                                    <Button onClick={() => setEditRowId(null)} className="btn btn-secondary btn-sm">❌</Button>
                                                </td>
                                            </tr>
                                        ) : (
                                            <tr key={order.order_id}>
                                                <td>{order.order_id}</td>
                                                <td>{order.merchandiser_id}</td>
                                                <td>{order.product_id}</td>
                                                <td>{order.quantity}</td>
                                                <td>{order.order_date}</td>
                                                <td>{order.status}</td>
                                                <td>{order.total_cost}</td>
                                                <td>
                                                    <Button className="btn btn-primary btn-sm me-2" onClick={(event) => handleEditClick(event, order)}>✏️</Button>
                                                    <Button className="btn btn-danger btn-sm" onClick={() => handleDeleteClick(order.order_id)}>🗑️</Button>
                                                </td>
                                            </tr>
                                        )
                                    ))}
                                </tbody>
                            </Table>
                        </form>
                    </div>
                </Col>
            </Row>

            <Modal show={showModal} onHide={handleCloseModal}>
                <Modal.Header closeButton>
                    <Modal.Title>Add New Order</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form onSubmit={handleNewOrderSubmit}>
                        <Row>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Merchandiser ID</Form.Label>
                                    <Form.Control type="text" name="merchandiser_id" value={newOrderData.merchandiser_id} onChange={handleNewOrderChange} />
                                </Form.Group>
                            </Col>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Product ID</Form.Label>
                                    <Form.Control type="text" name="product_id" value={newOrderData.product_id} onChange={handleNewOrderChange} />
                                </Form.Group>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Quantity</Form.Label>
                                    <Form.Control type="text" name="quantity" value={newOrderData.quantity} onChange={handleNewOrderChange} />
                                </Form.Group>
                            </Col>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Order Date</Form.Label>
                                    <Form.Control type="text" name="order_date" value={newOrderData.order_date} onChange={handleNewOrderChange} />
                                </Form.Group>
                            </Col>
                        </Row>
                        <Row>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Status</Form.Label>
                                    <Form.Control type="text" name="status" value={newOrderData.status} onChange={handleNewOrderChange} />
                                </Form.Group>
                            </Col>
                            <Col>
                                <Form.Group className="mb-3">
                                    <Form.Label>Total Cost</Form.Label>
                                    <Form.Control type="text" name="total_cost" value={newOrderData.total_cost} onChange={handleNewOrderChange} />
                                </Form.Group>
                            </Col>
                        </Row>
                        <Button variant="primary" type="submit">
                            Add Order
                        </Button>
                    </Form>
                </Modal.Body>
            </Modal>
        </Container>
    );
};
export default Order;
