import 'package:flutter/material.dart';
import 'register_page.dart';
import 'login_page.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // appBar: AppBar(
      //   centerTitle: true,
      //   title: const Text('Home',style: TextStyle(color: Colors.black87,fontSize: 50),),
      //   backgroundColor: Colors.blue,
      //
      // ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [Colors.blue.shade900, Colors.blue.shade100],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // Add the image here
              Padding(
                padding: const EdgeInsets.only(left: 30.0,bottom: 150),
                child: Image.asset(
                  'assets/wallet.png', // Replace with your image path
                  height: 200, // Adjust height according to your needs
                ),
              ),
              // SizedBox(height: 40), // Add space between image and buttons
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Padding(
                    padding: const EdgeInsets.only(bottom: 150),
                    child: SizedBox(
                      width: 200,
                      height: 50,

                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          primary: Colors.blue[900],

                        ),
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (context) => RegisterPage()),
                          );
                        },
                        child: const Text('Register',style: TextStyle(color: Colors.white),),
                      ),
                    ),
                  ),
                  SizedBox(width: 20), // Space between the two buttons
                  Padding(
                    padding: const EdgeInsets.only(bottom: 150),
                    child: SizedBox(
                      width: 200,
                      height: 50,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          primary: Colors.blue[900],

                        ),
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(builder: (context) => LoginPage()),
                          );
                        },
                        child: const Text('Login',style: TextStyle(color: Colors.white),),
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
