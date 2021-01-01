import React, { useState, useEffect } from "react";
import { Button, Image, View, Platform, Text, Alert } from "react-native";
import * as ImagePicker from "expo-image-picker";
import Constants from "expo-constants";

export default function App() {
  const [image, setImage] = useState(null);
  var rep = "resultat";
  useEffect(() => {
    (async () => {
      if (Platform.OS !== "web") {
        const {
          status,
        } = await ImagePicker.requestMediaLibraryPermissionsAsync();
        if (status !== "granted") {
          alert("Sorry, we need camera roll permissions to make this work!");
        }
      }
    })();
  }, []);

  uploadImage = async (image_uri) => {
    let base_url = 'http://192.168.43.88:5000/predictMobile';
    let uploadData = new FormData();
    uploadData.append('submit', 'ok');
    uploadData.append('file', {type: 'image/jpg', uri:image_uri, name: 'uploadimage.jpg'})
    fetch(base_url, {
      method: 'post',
      body: uploadData
    }).then(response => response.json())
    .then(response => {
      //rep = JSON.parse(response.data);
      rep = response;
      console.log(rep);
      Alert.alert(rep);
    })
  }

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      allowsEditing: true,
      quality: 1,
    });

    if (!result.cancelled) {
      uploadImage(result.uri);
      setImage(result.uri);
    }
  };

  return (
    <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
      <Button title="Pick an image" onPress={pickImage} />
      {image && (
        <Image source={{ uri: image }} style={{ width: 200, height: 200 }} />
      )}
    </View>
  );
}
