import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'dashboard_page.dart';
import 'package:wallet/api_service.dart';

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _phoneController = TextEditingController();
  final _passwordController = TextEditingController();
  final storage = new FlutterSecureStorage();

  bool _isLoading = false;
  String? _errorMessage;

  Future<void> _login() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    final phoneNumber = _phoneController.text;
    final password = _passwordController.text;

    final url = Uri.parse('${Config.baseUrl}/login/');
    final response = await http.post(
      url,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'phone_number': phoneNumber,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      var data = jsonDecode(response.body);
      String token = data['access'];

      // Save the token in secure storage
      await storage.write(key: 'jwt_token', value: token);

      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => DashboardPage()),
      );
    } else {
      setState(() {
        _errorMessage = 'Invalid phone number or password';
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
        title: const Text('Login', style: TextStyle(color: Colors.black)),
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
                Icons.app_shortcut,
                size: 150.0,  // Large size for the icon
                color: Colors.blue[900],  // Color for the icon
              ),
              SizedBox(height: 50),
              const Text(
                'Welcome back you\'ve been missed',
                style: TextStyle(
                  color: Colors.black,
                  fontSize: 20,
                ),
              ),
              SizedBox(height: 50),
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
              if (_errorMessage != null) ...[
                SizedBox(height: 8),
                Text(
                  _errorMessage!,
                  style: TextStyle(color: Colors.red),
                ),
              ],
              SizedBox(height: 16),
              _isLoading
                  ? CircularProgressIndicator()
                  : SizedBox(
                  width: 200,
                  height: 50,

                    child: ElevatedButton(
                                    style: ElevatedButton.styleFrom(
                    primary: Colors.blue[900],
                                    ),
                                    onPressed: _login,
                                    child: const Text('Login',style: TextStyle(color: Colors.white)),
                                  ),
                  ),
            ],
          ),
        ),
      ),
    );
  }
}
