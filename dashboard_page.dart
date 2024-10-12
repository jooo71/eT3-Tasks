//
// import 'package:flutter/material.dart';
// import 'deposit_page.dart';
// import 'withdraw_page.dart';
// import 'transfer_page.dart';
// import 'transaction_history_page.dart';
// import 'balance_page.dart';
//
// class DashboardPage extends StatelessWidget {
//   const DashboardPage({super.key});
//
//   @override
//   Widget build(BuildContext context) {
//     final height = MediaQuery.of(context).size.height;
//     final width = MediaQuery.of(context).size.width;
//
//     List<String> buttonLabels = [
//       'Deposit',
//       'Withdraw',
//       'Transfer',
//       'Transaction History',
//       'Balance',
//     ];
//
//     List<Widget> pages = [
//       DepositPage(),
//       WithdrawPage(),
//       TransferPage(),
//       TransactionHistoryPage(),
//       BalancePage(),
//     ];
//
//     List<IconData> buttonIcons = [
//       Icons.account_balance_wallet,
//       Icons.money_off,
//       Icons.send,
//       Icons.history,
//       Icons.account_balance,
//     ];
//
//     return Scaffold(
//       appBar: AppBar(
//         title: Text('Dashboard', style: TextStyle(color: Colors.white)),
//         backgroundColor: Colors.blue.shade900,
//       ),
//       body: Container(
//         width: width,
//         height: height,
//         decoration: BoxDecoration(
//           gradient: LinearGradient(
//             colors: [Colors.blue.shade900, Colors.blue.shade100],
//             begin: Alignment.topLeft,
//             end: Alignment.bottomRight,
//           ),
//         ),
//         child: Padding(
//           padding: const EdgeInsets.all(16.0),
//           child: Column(
//             mainAxisAlignment: MainAxisAlignment.center,
//             children: [
//               GridView.builder(
//                 shrinkWrap: true,
//                 itemCount: buttonLabels.length,
//                 gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
//                   crossAxisCount: 2,
//                   mainAxisSpacing: 20,
//                   crossAxisSpacing: 20,
//                   childAspectRatio: 1,
//                 ),
//                 itemBuilder: (context, index) {
//                   return Material(
//                     color: Colors.blue.shade900,
//                     elevation: 8,
//                     borderRadius: BorderRadius.circular(20),
//                     clipBehavior: Clip.antiAliasWithSaveLayer,
//                     child: InkWell(
//                       onTap: () {
//                         Navigator.push(
//                           context,
//                           MaterialPageRoute(builder: (context) => pages[index]),
//                         );
//                       },
//                       child: Container(
//                         padding: EdgeInsets.all(10),
//                         decoration: BoxDecoration(
//                           border: Border.all(
//                             width: 3,
//                             color: Colors.blue.shade900,
//                           ),
//                           borderRadius: BorderRadius.circular(20),
//                         ),
//                         child: Column(
//                           mainAxisAlignment: MainAxisAlignment.center,
//                           children: [
//                             Icon(
//                               buttonIcons[index],
//                               size: 40,
//                               color: Colors.white,
//                             ),
//                             SizedBox(height: 10),
//                             Text(
//                               buttonLabels[index],
//                               style: TextStyle(
//                                 color: Colors.white,
//                                 fontWeight: FontWeight.bold,
//                                 fontSize: 18,
//                               ),
//                               textAlign: TextAlign.center,
//                             ),
//                           ],
//                         ),
//                       ),
//                     ),
//                   );
//                 },
//               ),
//             ],
//           ),
//         ),
//       ),
//     );
//   }
// }
import 'package:flutter/material.dart';
import 'deposit_page.dart';
import 'withdraw_page.dart';
import 'transfer_page.dart';
import 'transaction_history_page.dart';
import 'balance_page.dart';

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    final height = MediaQuery.of(context).size.height;
    final width = MediaQuery.of(context).size.width;

    // Labels, pages, and icons for the operations
    List<String> buttonLabels = [
      'Deposit',
      'Withdraw',
      'Transfer',
      'Transaction History',
      'Balance',
    ];

    List<Widget> pages = [
      DepositPage(),
      WithdrawPage(),
      TransferPage(),
      TransactionHistoryPage(),
      BalancePage(),
    ];

    List<IconData> buttonIcons = [
      Icons.account_balance_wallet,
      Icons.money_off,
      Icons.send,
      Icons.history,
      Icons.account_balance,
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard', style: TextStyle(color: Colors.white)),
        backgroundColor: Colors.blue.shade900,
      ),
      body: Container(
        width: width,
        height: height,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [Colors.blue.shade900, Colors.blue.shade100],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: GridView.builder(
            shrinkWrap: true,
            itemCount: buttonLabels.length,
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,
              mainAxisSpacing: 20,
              crossAxisSpacing: 20,
              childAspectRatio: 1,
            ),
            itemBuilder: (context, index) {
              return Material(
                color: Colors.blue.shade900,
                elevation: 8,
                borderRadius: BorderRadius.circular(20),
                clipBehavior: Clip.antiAliasWithSaveLayer,
                child: InkWell(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => pages[index],
                      ),
                    );
                  },
                  child: Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      border: Border.all(
                        width: 3,
                        color: Colors.blue.shade900,
                      ),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          buttonIcons[index],
                          size: 40,
                          color: Colors.white,
                        ),
                        const SizedBox(height: 10),
                        Text(
                          buttonLabels[index],
                          style: const TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            fontSize: 18,
                          ),
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ),
    );
  }
}
