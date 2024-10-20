describe('API Tests', () => {
  
  // Base URL of your Django API (set this as needed)
  const apiUrl = 'http://localhost:8000/api';
    // Variable to store the JWT access token
    let accessToken = '';
    const testUser = {
      phone_number: '1234567890',  // Replace with your test data
      password: 'password123',     // Replace with your test data
      name: 'Test User'
    };

  it('should register a new user', () => {
    cy.request('POST', `${apiUrl}/register/`, {
      phone_number: testUser.phone_number,
      password: testUser.password,
      name: 'Test User'
    }).then((response) => {
      expect(response.status).to.eq(201);
      expect(response.body).to.have.property('access');
    });
  });

  it('should log in and get a token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/login/`,  // Your login endpoint
      body: {
        phone_number: testUser.phone_number,
        password: testUser.password,     // Replace with your test data
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if login is successful
      accessToken = response.body.access;  // Store the token
      expect(accessToken).to.exist;        // Ensure token is present
    });
  });
  
  it('should deposit money using the token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/deposit/`,  // Your deposit endpoint
      headers: {
        Authorization: `Bearer ${accessToken}`  // Pass the token in the Authorization header
      },
      body: {
        amount: 1000  // Amount to deposit
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if deposit is successful
      expect(response.body.message).to.include('Deposited');  // Verify the deposit message
    });
  });
  it('should withdraw money using the token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/withdraw/`,  // Your withdraw endpoint
      headers: {
        Authorization: `Bearer ${accessToken}`  // Pass the token in the Authorization header
      },
      body: {
        amount: 100  // Amount to withdraw
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if withdrawal is successful
      expect(response.body.message).to.include('Withdrew');  // Verify the withdraw message
    });
  });

  it('should transfer money using the token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/transfer/`,  // Your transfer endpoint
      headers: {
        Authorization: `Bearer ${accessToken}`  // Pass the token in the Authorization header
      },
      body: {
        recipient_phone: '01110989460',  // Replace with the recipient's phone number
        amount: 300  // Amount to transfer
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if transfer is successful
      expect(response.body.message).to.include('Transferred');  // Verify the transfer message
      expect(response.body.recipient_name).to.exist;  // Ensure recipient name is returned
    });
  });

  it('should pay a bill using the token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/pay-bill/`,  // Your pay bill endpoint
      headers: {
        Authorization: `Bearer ${accessToken}`  // Pass the token in the Authorization header
      },
      body: {
        bill_type: 'Electricity',  // Type of bill (replace with your test data)
        amount: 150  // Amount to pay
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if bill payment is successful
      expect(response.body.message).to.include('paid');  // Verify the bill payment message
      expect(response.body.message).to.include('Electricity');  // Ensure bill type is returned
    });
  });

  it('should buy airtime using the token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/buy-airtime/`,  // Your buy airtime endpoint
      headers: {
        Authorization: `Bearer ${accessToken}`  // Pass the token in the Authorization header
      },
      body: {
        amount: 100  // Amount to buy airtime
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if airtime purchase is successful
      expect(response.body.message).to.include('Bought');  // Verify the airtime purchase message
      expect(response.body.message).to.include('worth of airtime');  // Ensure the message mentions airtime
    });
  });
  it('should retrieve transaction history using the token', () => {
    cy.request({
      method: 'GET',
      url: `${apiUrl}/transaction-history/`,  // Your transaction history endpoint
      headers: {
        Authorization: `Bearer ${accessToken}`  // Pass the token in the Authorization header
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if retrieval is successful
      expect(response.body).to.be.an('array');  // Ensure the response is an array
      
      // Optionally check if the array is not empty
      if (response.body.length > 0) {
        const transaction = response.body[0];  // Get the first transaction
        // Check for general fields that should be present in a transaction
        expect(transaction).to.have.property('id');  // Assuming each transaction has an ID
        expect(transaction).to.have.property('amount');  // Assuming each transaction has an amount
        expect(transaction).to.have.property('transaction_type');  // Assuming type of transaction
        expect(transaction).to.have.property('date');  // Assuming there is a date field
        // Add more fields here as necessary based on your Transaction model
      }
    });
  });
  it('should retrieve balance using the token', () => {
    cy.request({
      method: 'GET',
      url: `${apiUrl}/balance/`,  // Your balance endpoint
      headers: {
        Authorization: `Bearer ${accessToken}`  // Pass the token in the Authorization header
      }
    }).then((response) => {
      expect(response.status).to.eq(200);  // Check if retrieval is successful
      expect(response.body).to.have.property('balance');  // Ensure the response includes the balance
      expect(response.body).to.have.property('message');  // Ensure the response includes a message
      expect(response.body.balance).to.be.a('number');  // Ensure the balance is a number
    });
  });
});

///////////////////////////////////////////////////////////////////////////////////

describe('Full Flow', () => {

  const apiUrl = 'http://localhost:8000/api';

  const testUser2 = {
    phone_number: '1234567899',  // Replace with your test data
    password: 'password123',     // Replace with your test data
    name: 'Test2 User'
  };

  let accessToken = '';

  // Step 1: Register the user if not already registered
  it('should register a new user if not already registered', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/register/`,
      body: {
        phone_number: testUser2.phone_number,
        password: testUser2.password,
        name: testUser2.name
      },
    }).then((response) => {
      if (response.status === 201) {
        cy.log('User registered successfully.');
      } else if (response.status === 400 && response.body.error === 'Phone number already registered.') {
        cy.log('User already exists. Skipping registration.');
      } else {
        throw new Error('Failed to register the user.');
      }
    });
  });

  // Step 2: Log in the user and store the token
  it('should log in the user and get a token', () => {
    cy.request({
      method: 'POST',
      url: `${apiUrl}/login/`,
      body: {
        phone_number: testUser2.phone_number,
        password: testUser2.password
      },
    }).then((response) => {
      if (response.status === 200) {
        accessToken = response.body.access;
        expect(accessToken).to.exist;
        cy.log('Login successful, token acquired.');
      } else {
        throw new Error('Login failed. Cannot proceed with further tests.');
      }
    });
  });

  // Step 3: Perform deposit action
  it('should perform deposit using the token', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/deposit/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: 1000  // Example amount
      }
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('message');
      cy.log('Deposit successful.');
    });
  });

  // Step 4: Perform withdraw action
  it('should perform withdraw using the token', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/withdraw/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: 50  // Example amount
      }
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('message');
      cy.log('Withdraw successful.');
    });
  });

  // Step 5: Perform transfer action
  it('should perform transfer using the token', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/transfer/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        recipient_phone: '01110989460',  // Replace with a valid recipient phone number
        amount: 10000  // Example amount
      }
    }).then((response) => {
      if (response.status === 200) {
        cy.log('Transfer successful.');
        expect(response.body).to.have.property('recipient_name');
      } else if (response.status === 400 || response.status === 404) {
        cy.log('Transfer failed: ' + response.body.error);
      }
    });
  });

  // Step 6: Perform pay bill action
  it('should pay bill using the token', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/pay-bill/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        bill_type: 'electricity',  // Example bill type
        amount: 75  // Example amount
      }
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('message');
      cy.log('Bill payment successful.');
    });
  });

  // Step 7: Perform buy airtime action
  it('should buy airtime using the token', () => {
    if (!accessToken) return;

    cy.request({
      method: 'POST',
      url: `${apiUrl}/buy-airtime/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      },
      body: {
        amount: 20  // Example amount
      }
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('message');
      cy.log('Airtime purchase successful.');
    });
  });

  // Step 8: Retrieve transaction history
  it('should retrieve transaction history using the token', () => {
    if (!accessToken) return;

    cy.request({
      method: 'GET',
      url: `${apiUrl}/transaction-history/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.be.an('array');  // Expect the transaction history to be an array
      cy.log('Transaction history retrieved.');
    });
  });

  // Step 9: Retrieve balance
  it('should retrieve balance using the token', () => {
    if (!accessToken) return;

    cy.request({
      method: 'GET',
      url: `${apiUrl}/balance/`,
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.property('balance');
      cy.log('Balance retrieved.');
    });
  });

});
