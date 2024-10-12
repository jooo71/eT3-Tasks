import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../api_service.dart';

class RegisterPage extends StatefulWidget {
  @override
  _RegisterPageState createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _phoneController = TextEditingController();
  final _nameController = TextEditingController();
  final _passwordController = TextEditingController();

  bool _isLoading = false;
  String? _errorMessage;
  String? _successMessage;

  Future<void> _register() async {
    // Validate inputs
    if (_phoneController.text.isEmpty || _nameController.text.isEmpty || _passwordController.text.isEmpty) {
      setState(() {
        _errorMessage = 'Please fill in all fields.';
      });
      return; // Exit the function if validation fails
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _successMessage = null;
    });

    final phoneNumber = _phoneController.text;
    final name = _nameController.text;
    final password = _passwordController.text;

    final url = Uri.parse('${Config.baseUrl}/register/');
    final response = await http.post(
      url,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'phone_number': phoneNumber,
        'name': name,
        'password': password,
      }),
    );

    if (response.statusCode == 201) {
      setState(() {
        _successMessage = 'Registration successful! You can now log in.';
      });
    } else {
      setState(() {
        _errorMessage = 'Registration failed. Please try again.';
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
        title: const Text('Register', style: TextStyle(color: Colors.black)),
        backgroundColor: Colors.blue.shade900,
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [Colors.blue.shade900, Colors.blue.shade100],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
               Icon(
                Icons.app_registration,
                size: 150.0,  // Large size for the icon
                color: Colors.blue[900],  // Color for the icon
              ),
              const SizedBox(height: 60),
              TextField(
                controller: _phoneController,
                decoration: InputDecoration(
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(80.0),
                    borderSide: const BorderSide(color: Colors.black),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(80.0),
                    borderSide: const BorderSide(color: Colors.black),
                  ),
                  filled: true,
                  fillColor: Colors.grey.shade50,
                  hintText: 'Phone Number',
                  hintStyle: TextStyle(color: Colors.grey.shade700, fontSize: 15),
                  prefixIcon: const Icon(Icons.phone),
                ),
                keyboardType: TextInputType.phone,
              ),
              const SizedBox(height: 15),
              TextField(
                controller: _nameController,
                decoration: InputDecoration(
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(80.0),
                    borderSide: const BorderSide(color: Colors.black),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(80.0),
                    borderSide: const BorderSide(color: Colors.black),
                  ),
                  filled: true,
                  fillColor: Colors.grey.shade50,
                  hintText: 'Name',
                  hintStyle: TextStyle(color: Colors.grey.shade700, fontSize: 15),
                  prefixIcon: const Icon(Icons.abc_sharp, size: 30),
                ),
              ),
              const SizedBox(height: 15),
              TextField(
                controller: _passwordController,
                decoration: InputDecoration(
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(80.0),
                    borderSide: const BorderSide(color: Colors.black),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(80.0),
                    borderSide: const BorderSide(color: Colors.black),
                  ),
                  filled: true,
                  fillColor: Colors.grey.shade50,
                  hintText: 'Password',
                  hintStyle: TextStyle(color: Colors.grey.shade700, fontSize: 15),
                  prefixIcon: const Icon(Icons.password_outlined, size: 30),
                ),
                obscureText: true,
              ),
              SizedBox(height: 16),
              if (_isLoading)
                CircularProgressIndicator()
              else
                SizedBox(
                  width: 200,
                  height: 50,
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      primary: Colors.blue[900],
                    ),
                    onPressed: _register,
                    child: Text('Register', style: TextStyle(color: Colors.white)),
                  ),
                ),
              if (_successMessage != null) ...[
                SizedBox(height: 16),
                Text(
                  _successMessage!,
                  style: TextStyle(color: Color(0xFF062806), fontSize: 20),
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
      ),
    );
  }
}
