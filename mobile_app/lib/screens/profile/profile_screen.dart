import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Profile')),
      body: ListView(
        children: [
          ListTile(
            leading: Icon(Icons.person),
            title: Text('User Name'),
            // TODO: Implement profile details
          ),
          ListTile(
            leading: Icon(Icons.analytics),
            title: Text('Knowledge Level'),
            // TODO: Implement knowledge level display
          ),
          ListTile(
            leading: Icon(Icons.settings),
            title: Text('Settings'),
            onTap: () {
              // TODO: Implement settings navigation
            },
          ),
        ],
      ),
    );
  }
}