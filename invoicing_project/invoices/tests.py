from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Invoice, InvoiceDetail

class InvoiceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.invoice_data = {'date': '2024-02-23', 'customer_name': 'Test Customer'}
        self.invoice_detail_data = {'description': 'Test Description', 'quantity': 2, 'unit_price': 10.0, 'price': 20.0}

    def test_create_invoice_with_details(self):
        response = self.client.post('/api/invoices/', {'date': '2024-02-23', 'customer_name': 'Test Customer', 'details': [self.invoice_detail_data]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(InvoiceDetail.objects.count(), 1)

    def test_update_invoice_with_details(self):
        invoice = Invoice.objects.create(**self.invoice_data)
        detail = InvoiceDetail.objects.create(invoice=invoice, **self.invoice_detail_data)

        updated_data = {'date': '2024-02-24', 'customer_name': 'Updated Customer', 'details': [{'description': 'Updated Description', 'quantity': 3, 'unit_price': 15.0, 'price': 45.0}]}

        response = self.client.put(f'/api/invoices/{invoice.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(InvoiceDetail.objects.count(), 1)

        updated_invoice = Invoice.objects.get(id=invoice.id)
        self.assertEqual(updated_invoice.date, '2024-02-24')
        self.assertEqual(updated_invoice.customer_name, 'Updated Customer')

        updated_detail = InvoiceDetail.objects.get(id=detail.id)
        self.assertEqual(updated_detail.description, 'Updated Description')
        self.assertEqual(updated_detail.quantity, 3)
        self.assertEqual(updated_detail.unit_price, 15.0)
        self.assertEqual(updated_detail.price, 45.0)