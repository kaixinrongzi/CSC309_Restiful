import React, { useState } from 'react';
import './css/style1.css';
import './css/style2.css';
import './css/index.css';
import './css/bulma/bulma.css';
import './css/bulma/bulma.css.map';
import './css/bulma/bulma.min.css';
import './css/bulma/bulma-rtl.css';
import './css/bulma/bulma-rtl.css.map';
import './css/bulma/bulma-rtl.min.css';
import './css/regLog.css';
import { Navigate } from 'react-router-dom';
import $ from 'jquery';
import axios from 'axios';

export default function PropertyRegister() {
  const [isRegistered, setIsRegistered] = useState(false);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [error, setError] = useState('');

  const validateForm = (e) => {
    e.preventDefault();

    // Check if the name field is empty
    const nameInput = document.getElementById("name");
    if (nameInput.value === "") {
      setError("Name field is required");
      return;
    }

    // Check if the address field is empty
    const addressInput = document.getElementById("address");
    if (addressInput.value === "") {
      setError("Address field is required");
      return;
    }
        // Continue with the rest of the validation and form submission logic
        propertyRegisterHandler(e);
    };

  const propertyRegisterHandler = (e) => {
    
    e.preventDefault();
    var myForm = $(e.target.closest('form'));
    axios
      .post('http://localhost:8000/hotels/add/', {
        name: myForm.find('#name').val(),
        address: myForm.find('#address').val(),
        description: myForm.find('#description').val(),
        capacity: myForm.find('#capacity').val(),
        beds: myForm.find('#beds').val(),
        baths: myForm.find('#baths').val(),
      })
      .then((response) => {
        console.log(response.data);

        alert('Property Registered Successfully!');
        setIsRegistered(true);
      })
      .catch((error) => {
        console.log(error.response);
        if (error.response.status === 400) {
          setError('Error: ' + JSON.stringify(error.response.data));
        }
      });
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onloadend = () => {
      setUploadedImage(reader.result);
    };

    if (file) {
      reader.readAsDataURL(file);
    } else {
      setUploadedImage(null);
    }
  };

  if (!isRegistered) {
    return (
      <div className="property_register_overall">
        <div className="register">
          <form className="form" id="form2">
            <h2 className="form__title">Register Property</h2>
            <input type="text" placeholder="Name" className="input" id="name" required></input>
            <input type="text" placeholder="Address" className="input" id="address" required></input>
            <textarea placeholder="Description" className="input" id="description"></textarea>
            <input type="number" placeholder="Capacity" className="input" id="capacity" required></input>
            <input type="number" placeholder="Beds" className="input" id="beds" required></input>
            <input type="number" placeholder="Baths" className="input" id="baths" required></input>
            <input className="btn" type="submit" value="Register Property" id="register" onClick={validateForm}></input>
            <input type="file" accept="image/*" className="input" id="propertyImage" onChange={handleImageUpload}/>
          </form>
          <p id="error">{error}</p>
          {uploadedImage && (
        <div>
          <h3>Uploaded Image:</h3>
          <img src={uploadedImage} alt="Uploaded Property" style={{ width: '100%', maxWidth: '300px' }} />
        </div>
      )}
        </div>
      </div>
    );
  } else {
    return <Navigate to="/profile/" />;
  }
}
