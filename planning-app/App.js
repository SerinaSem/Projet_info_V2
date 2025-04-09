import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  Image,
  TouchableOpacity,
  StyleSheet,
  Alert,
  SafeAreaView
} from 'react-native';
import axios from 'axios';

export default function App() {
  const [email, setEmail] = useState('');
  const [motDePasse, setMotDePasse] = useState('');
  const [role, setRole] = useState('employe');

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://10.188.51.157:5000/login', {
        email,
        mot_de_passe: motDePasse,
        role: role, // si besoin côté backend
      });

      if (response.data.success) {
        const { nom, prenom } = response.data.employe;
        Alert.alert('Connexion réussie', `Bienvenue ${prenom} ${nom}`);
        // Ici on pourra rediriger vers l'écran du planning
      } else {
        Alert.alert('Erreur', response.data.message);
      }
    } catch (err) {
      Alert.alert('Erreur', "Impossible de se connecter au serveur.");
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.leftPane}>
        <Image
          source={require('./assets/login_illustration.png')}
          style={styles.image}
          resizeMode="contain"
        />
      </View>

      <View style={styles.rightPane}>
        <Text style={styles.title}>Bienvenue 👋</Text>
        <Text style={styles.subtitle}>Connectez-vous à votre espace</Text>

        <View style={styles.roleSwitch}>
          <TouchableOpacity
            style={[styles.roleButton, role === 'employe' && styles.selectedRole]}
            onPress={() => setRole('employe')}
          >
            <Text style={styles.roleText}>Employé</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.roleButton, role === 'employeur' && styles.selectedRole]}
            onPress={() => setRole('employeur')}
          >
            <Text style={styles.roleText}>Employeur</Text>
          </TouchableOpacity>
        </View>

        <TextInput
          style={styles.input}
          placeholder="Email"
          placeholderTextColor="#888"
          value={email}
          onChangeText={setEmail}
        />
        <TextInput
          style={styles.input}
          placeholder="Mot de passe"
          placeholderTextColor="#888"
          secureTextEntry
          value={motDePasse}
          onChangeText={setMotDePasse}
        />
        <TouchableOpacity style={styles.loginButton} onPress={handleLogin}>
          <Text style={styles.loginButtonText}>Se connecter</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    flex: 1,
    backgroundColor: '#f5f1e6',
  },
  leftPane: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fbeacc',
    padding: 20,
  },
  image: {
    width: '100%',
    height: '80%',
  },
  rightPane: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 40,
    backgroundColor: '#fff9f0',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#5e412f',
  },
  subtitle: {
    fontSize: 16,
    color: '#5e412f',
    marginBottom: 30,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 25,
    padding: 12,
    marginBottom: 15,
    paddingHorizontal: 20,
    backgroundColor: '#fff',
  },
  loginButton: {
    backgroundColor: '#d4a373',
    padding: 15,
    borderRadius: 25,
    alignItems: 'center',
    marginTop: 10,
  },
  loginButtonText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  roleSwitch: {
    flexDirection: 'row',
    marginBottom: 15,
    justifyContent: 'center',
  },
  roleButton: {
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#ccc',
    marginHorizontal: 5,
    backgroundColor: '#f0e5d8',
  },
  selectedRole: {
    backgroundColor: '#d4a373',
    borderColor: '#d4a373',
  },
  roleText: {
    color: '#333',
    fontWeight: 'bold',
  },
});
