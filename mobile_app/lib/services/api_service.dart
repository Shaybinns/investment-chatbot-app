import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = 'http://localhost:8000/api/v1';

  Future<Map<String, dynamic>> login(String email, String password) async {
    // TODO: Implement login
    throw UnimplementedError();
  }

  Future<Map<String, dynamic>> getPortfolios() async {
    // TODO: Implement get portfolios
    throw UnimplementedError();
  }

  Future<Map<String, dynamic>> sendMessage(String message) async {
    // TODO: Implement send message
    throw UnimplementedError();
  }
}