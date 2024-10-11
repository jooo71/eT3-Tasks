import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../api_service.dart';

class TransferPage extends StatefulWidget {
  @override
  _TransferPageState createState() => _TransferPageState();
}

class _TransferPageState extends State<TransferPage> {
  final _recipientPhoneController = TextEditingController();
  final _amountController = TextEditingController();
  final storage = new FlutterSecureStorage();
  bool _isLoading = false;
  String? _successMessage;
  String? _errorMessage;

  Future<void> _transfer() async {
    setState(() {
      _isLoading = true;
      _successMessage = null;
      _errorMessage = null;
    });

    String? token = await storage.read(key: 'jwt_token');
    final recipientPhone = _recipientPhoneController.text;
    final amount = _amountController.text;

    final url = Uri.parse('${Config.baseUrl}/transfer/');
    final response = await http.post(
      url,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode(<String, String>{
        'recipient_phone': recipientPhone,
        'amount': amount,
      }),
    );

    if (response.statusCode == 200) {
      var data = jsonDecode(response.body);
      setState(() {
        _successMessage = data['message'];
      });
    } else {
      setState(() {
        _errorMessage = 'Transfer failed. Please check the recipient phone number and your balance.';
      });
    }

    setState(() {
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Transfer'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _recipientPhoneController,
              decoration: InputDecoration(labelText: 'Recipient Phone Number'),
              keyboardType: TextInputType.phone,
            ),
            SizedBox(height: 16),
            TextField(
              controller: _amountController,
              decoration: InputDecoration(labelText: 'Amount'),
              keyboardType: TextInputType.number,
            ),
            SizedBox(height: 16),
            _isLoading
                ? CircularProgressIndicator()
                : ElevatedButton(
              onPressed: _transfer,
              child: Text('Transfer'),
            ),
            if (_successMessage != null) ...[
              SizedBox(height: 16),
              Text(
                _successMessage!,
                style: TextStyle(color: Colors.green),
              ),
            ],
            if (_errorMessage != null) ...[
              SizedBox(height: 16),
              Text(
                _errorMessage!,
                style: TextStyle(color: Colors.red),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
