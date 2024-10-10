import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class TransactionHistoryPage extends StatefulWidget {
  @override
  _TransactionHistoryPageState createState() => _TransactionHistoryPageState();
}

class _TransactionHistoryPageState extends State<TransactionHistoryPage> {
  final storage = new FlutterSecureStorage();
  bool _isLoading = false;
  List<dynamic> _transactions = [];
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchTransactionHistory();
  }

  Future<void> _fetchTransactionHistory() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    String? token = await storage.read(key: 'jwt_token');

    final url = Uri.parse('http://127.0.0.1:8000/api/transaction-history/');
    final response = await http.get(
      url,
      headers: {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      var data = jsonDecode(response.body);
      setState(() {
        _transactions = data;
      });
    } else {
      setState(() {
        _errorMessage = 'Failed to fetch transaction history';
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
        title: Text('Transaction History'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: _isLoading
            ? Center(child: CircularProgressIndicator())
            : _errorMessage != null
            ? Center(
          child: Text(
            _errorMessage!,
            style: TextStyle(color: Colors.red),
          ),
        )
            : _transactions.isEmpty
            ? Center(child: Text('No transactions available'))
            : ListView.builder(
          itemCount: _transactions.length,
          itemBuilder: (context, index) {
            var transaction = _transactions[index];
            return ListTile(
              title: Text(transaction['transaction_type']),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                      'Amount: ${transaction['amount']}'),
                  if (transaction['recipient'] != null)
                    Text(
                        'Recipient: ${transaction['recipient']}'),
                  Text('Date: ${transaction['date']}'),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}
