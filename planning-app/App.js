import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  Image,
  TouchableOpacity,
  StyleSheet,
  Alert,
  SafeAreaView,
} from 'react-native';
import axios from 'axios';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

const LoginScreen = ({ navigation }) => {
  const [email, setEmail] = useState('');
  const [motDePasse, setMotDePasse] = useState('');
  const [role, setRole] = useState('employe');
  const [codeEmployeur, setCodeEmployeur] = useState('');

  const handleLogin = async () => {
    try {
      const payload = role === 'employeur'
        ? { code: codeEmployeur, role }
        : { email, mot_de_passe: motDePasse, role };

      const response = await axios.post('http://127.0.0.1:5000/login', payload);

      if (response.data.success) {
        if (role === 'employe') {
          navigation.navigate('Planning', { employe: response.data.employe });
        } else {
          navigation.navigate('EmployeurDashboard');
        }
      } else {
        Alert.alert('Erreur', response.data.message);
      }
    } catch (err) {
      Alert.alert('Erreur', 'Impossible de se connecter au serveur.');
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.leftPane}>
        <Image source={require('./assets/login_illustration.png')} style={styles.image} resizeMode="contain" />
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

        {role === 'employe' ? (
          <>
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
          </>
        ) : (
          <TextInput
            style={styles.input}
            placeholder="Code employeur"
            placeholderTextColor="#888"
            secureTextEntry
            value={codeEmployeur}
            onChangeText={setCodeEmployeur}
          />
        )}

        <TouchableOpacity style={styles.loginButton} onPress={handleLogin}>
          <Text style={styles.loginButtonText}>Se connecter</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const PlanningScreen = ({ route }) => {
  const { employe } = route.params;
  const [planning, setPlanning] = useState([]);

  useEffect(() => {
    axios
      .get(`http://127.0.0.1:5000/planning/${employe.id}`)
      .then((res) => setPlanning(res.data))
      .catch((err) => Alert.alert('Erreur', 'Impossible de récupérer le planning.'));
  }, []);

  return (
    <SafeAreaView style={{ flex: 1, padding: 20, backgroundColor: '#f5f1e6' }}>
      <Text style={{ fontSize: 26, fontWeight: 'bold', marginBottom: 10, color: '#5e412f' }}>
        Bonjour {employe.prenom} 👋
      </Text>
      <Text style={{ fontSize: 16, marginBottom: 20, color: '#5e412f' }}>
        Voici ton planning de la semaine. Bon courage 💪 et bonne énergie pour chaque service !
      </Text>

      <View style={{ backgroundColor: '#fff', borderRadius: 10, overflow: 'hidden' }}>
        <View style={{ flexDirection: 'row', backgroundColor: '#d4a373' }}>
          <Text style={styles.tableHeader}>Jour</Text>
          <Text style={styles.tableHeader}>Heure début</Text>
          <Text style={styles.tableHeader}>Heure fin</Text>
        </View>
        {planning.map((h, index) => (
          <View
            key={index}
            style={{
              flexDirection: 'row',
              backgroundColor: index % 2 === 0 ? '#fff9f0' : '#f0e5d8',
              paddingVertical: 10,
              paddingHorizontal: 5,
            }}
          >
            <Text style={styles.tableCell}>{h.jour}</Text>
            <Text style={styles.tableCell}>{h.heure_debut}</Text>
            <Text style={styles.tableCell}>{h.heure_fin}</Text>
          </View>
        ))}
      </View>
    </SafeAreaView>
  );
};

const EmployeurDashboard = () => {
  return (
    <SafeAreaView style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text style={{ fontSize: 20 }}>Bienvenue dans l'espace employeur !</Text>
      {/* On ajoutera le tableau ici à l'étape suivante */}
    </SafeAreaView>
  );
};

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: true }}>
        <Stack.Screen name="Login" component={LoginScreen} options={{ title: 'Connexion' }} />
        <Stack.Screen name="Planning" component={PlanningScreen} options={{ title: 'Planning' }} />
        <Stack.Screen name="EmployeurDashboard" component={EmployeurDashboard} options={{ title: 'Tableau employeur' }} />
      </Stack.Navigator>
    </NavigationContainer>
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
  tableHeader: {
    flex: 1,
    fontWeight: 'bold',
    padding: 10,
    color: '#fff',
    textAlign: 'center',
  },
  tableCell: {
    flex: 1,
    textAlign: 'center',
    color: '#5e412f',
  },
});
