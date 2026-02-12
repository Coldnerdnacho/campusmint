# CampusMint

Decentralized campus finance on Algorand. Smart contracts enforcing savings, fraud-proof tickets, and transparent fundraising.

## What is CampusMint?

CampusMint is a blockchain-based financial platform for college campuses. It solves three problems students face:

1. **Savings Enforcement** - Time-locked savings accounts that cannot be withdrawn from early
2. **Ticket Fraud** - NFT-based event tickets that cannot be screenshot or duplicated
3. **Transparent Fundraising** - Club treasuries where every donation is visible on the blockchain

All three features operate independently with their own tokens, but work together to create a complete financial ecosystem for campus communities.

## The Three Core Features

### Savings Vault

Students lock money for a specific period. The smart contract enforces the lock. They cannot withdraw early, even if they want to. This removes temptation and guarantees savings.

Example: A student locks ₹5,000 for exam fees until May 2025. The contract will not release the money before that date.

**Current Status**: Ready to deploy. Smart contract written. Waiting for deployment.

### Event Tickets

Clubs mint unique NFT tickets. Each ticket is a unique asset on the blockchain. Students buy tickets and receive the NFT as proof. At the event, organizers verify blockchain ownership. No duplicates possible.

Example: A fest creates 500-seat concert. They mint 500 NFTs. Students buy tickets. Entry is verified by checking blockchain ownership. Screenshot scams are impossible.

**Current Status**: Smart contract designed. Waiting for implementation.

### Treasury Pool

Clubs set a fundraising goal and deadline. Students contribute. Every contribution is recorded on blockchain. Progress updates in real-time. When deadline passes, if goal is met, funds transfer to the club automatically.

Example: Tech club needs ₹100,000 for hackathon. Creates fundraiser. Students contribute. Blockchain shows ₹50,000 raised. On deadline, if goal is met, club receives funds automatically.

**Current Status**: Live and working. App ID: 755379222. ₹50,000 already raised toward ₹100,000 goal.

## The Application

The app provides an intuitive interface to interact with these three features. Person 4 has built the frontend with three main screens:

### Home Page

The landing screen showing all available options. Students see:
- Quick access to their savings vaults
- Available events and tickets
- Active fundraising campaigns
- Account summary

### Savings Screen

Students can:
- Create a new savings vault
- Specify amount to lock
- Choose unlock date
- View their locked savings
- See countdown to unlock
- Withdraw once unlocked

### Tickets Screen

Students can:
- Browse available events
- View ticket details
- Purchase event tickets
- See owned tickets
- Verify ticket ownership at events

## Project Status

### Completed (60%)

- **Smart Contracts**: Three contracts written and tested (vault, treasury, tickets)
- **Dashboard**: Python interface connecting to blockchain
- **Treasury**: Live on Algorand testnet with ₹50,000 already contributed
- **App Frontend**: Three screens built by Person 4 (home, savings, tickets)
- **Documentation**: Complete guides for vision, architecture, and implementation
- **Tokens**: CampusCoin and Campus INR live on testnet

### In Progress (30%)

- **Vault Contract**: Ready to deploy
- **Vault Token**: Ready to create
- **Ticket System**: Implementation in progress

### To Do (10%)

- **Backend API**: Coordinate between app frontend and blockchain
- **Mobile Optimization**: Make responsive for all devices
- **Production Deployment**: Move from testnet to mainnet

## Technology Stack

- **Blockchain**: Algorand testnet
- **Smart Contracts**: TEAL 6.0
- **Backend**: Python with py-algorand-sdk
- **Frontend**: React/Flutter (built by Person 4)
- **Database**: None (all state on blockchain)

## Quick Start

### For Users

1. Visit the app (hosted at [URL to be added])
2. Connect your Algorand wallet
3. Choose a feature:
   - Create a savings vault
   - Buy event tickets
   - Contribute to a fundraiser
4. Sign transactions with your wallet
5. View updates in real-time

### For Developers

```bash
# Clone repository
git clone https://github.com/yourusername/campusmint.git
cd campusmint

# Install dependencies
pip install -r requirements.txt

# Set up local testnet
goal network create -t testnet

# Deploy contracts
python deploy_contracts.py

# Start dashboard
jupyter notebook dashboard/campusmint_dashboard.ipynb

# Start app backend
python app/main.py
```

## Project Structure

```
campusmint/
├── README.md                          (this file)
├── smart-contracts/
│   ├── vault.teal                    (student savings contract)
│   ├── treasury.teal                 (fundraising contract)
│   └── tickets.teal                  (event ticket system)
├── app/
│   ├── screens/
│   │   ├── home.jsx                  (home page)
│   │   ├── savings.jsx               (savings vault screen)
│   │   └── tickets.jsx               (event tickets screen)
│   ├── main.py                       (backend server)
│   ├── blockchain.py                 (blockchain integration)
│   └── config.py                     (configuration)
├── dashboard/
│   ├── campusmint_dashboard.ipynb    (colab notebook)
│   └── blockchain_reader.py          (state reading functions)
├── docs/
│   ├── PROJECT_DOCUMENTATION.md      (vision and architecture)
│   ├── TECHNICAL_IMPLEMENTATION.md   (implementation details)
│   ├── QUICK_REFERENCE.md            (quick overview)
│   └── APP_GUIDE.md                  (how to use the app)
└── config.example.json               (configuration template)
```

## Current Deployment

### Live on Algorand Testnet

- **Treasury Pool**: App ID 755379222
- **CampusCoin Token**: Asset 755379212 (fundraising)
- **Campus INR Token**: Asset 755378709 (ticket payments)

### Verify on Blockchain

- Treasury Pool: https://testnet.algoexplorer.io/application/755379222
- CampusCoin: https://testnet.algoexplorer.io/asset/755379212
- Campus INR: https://testnet.algoexplorer.io/asset/755378709

## How It Works

### Three Independent Systems

CampusMint's architecture is modular. Each feature has:
- Its own smart contract
- Its own token
- Its own rules and logic
- Independent operation

This means problems in one system don't affect others. If vault has an issue, tickets and fundraising continue working.

### User Flow

1. **Student opens app** and sees three options
2. **Selects a feature** (savings, tickets, or fundraise)
3. **App displays relevant screen**
4. **Student takes action** (create vault, buy ticket, contribute)
5. **App constructs blockchain transaction**
6. **Student signs with their wallet**
7. **Transaction sent to blockchain**
8. **Smart contract executes**
9. **State updates on blockchain**
10. **App refreshes to show new state**

### Why Blockchain?

Three critical advantages:

**Enforcement**: Rules are enforced in code. A vault cannot be withdrawn from early. Even the organization cannot override this.

**Transparency**: Every transaction is recorded. Everyone can verify fundraising amounts. No hidden money.

**Affordability**: Algorand transactions cost less than one paise. Transactions are economical at scale.

## The Three Screens Person 4 Built

### Home Screen

Central dashboard showing:
- User's account balance
- Active vaults and unlock dates
- Owned event tickets
- Available fundraising campaigns
- Quick action buttons for each feature

The home screen serves as the entry point. Students see an overview of their financial activity across all three features.

### Savings Screen

Dedicated interface for vault operations:

**Creating a Vault**:
- Input: Amount to lock (in rupees)
- Input: Unlock date (calendar picker)
- Input: Purpose (description)
- Action: Create vault
- Confirmation: Transaction ID and vault details

**Viewing Vaults**:
- List of all active vaults
- Locked amount
- Unlock date with countdown
- Current status (locked/unlocked)
- Withdraw button (appears after unlock)

The savings screen removes friction from time-locked savings. The interface makes it simple to create vaults and track their status.

### Tickets Screen

Event ticketing interface:

**Browsing Events**:
- List of upcoming events
- Event name, date, location
- Ticket price
- Available tickets remaining
- Event organizer information

**Purchasing Tickets**:
- Select event
- Specify quantity
- Review price
- Confirm payment
- Receive NFT ticket

**Viewing Owned Tickets**:
- List of purchased tickets
- Event details
- Ticket ID and verification code
- Transfer option (for secondary market)

The tickets screen makes the purchasing process smooth and verification easy.

## Security Model

### Private Keys

Students keep their own private keys. The app never stores or accesses them. Students sign every transaction themselves.

If the app is hacked, funds are safe. The hacker cannot access private keys or create unauthorized transactions.

### Smart Contracts

Rules are enforced at the blockchain level, not in the app. A vault cannot be unlocked early because the contract prevents it. No backdoor exists.

### Test Environment

The system runs on Algorand testnet, not mainnet. This is intentional. Testing can happen safely without financial risk.

## Getting Started with the Code

### Prerequisites

- Node.js 14+ (for React frontend)
- Python 3.8+ (for backend)
- Algorand sandbox or access to testnet
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/campusmint.git
cd campusmint

# Install frontend dependencies
cd app
npm install

# Install backend dependencies
pip install -r ../requirements.txt
```

### Running the Application

```bash
# Terminal 1: Start backend
cd campusmint/app
python main.py
# Backend runs on http://localhost:5000

# Terminal 2: Start frontend
cd campusmint/app
npm start
# Frontend runs on http://localhost:3000
```

### Testing with Testnet

```bash
# Get testnet ALGO
# Visit: https://testnet-dispenser.algorand.org/
# Request ALGO for your address

# Configure app
cp config.example.json config.json
# Edit config.json with your testnet details

# Run the app
# Use testnet ALGO to test all features
```

## Contributing

We welcome contributions. See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

Areas we need help with:
- Smart contract implementation (vault, tickets)
- Backend API development
- Frontend improvements
- Testing and QA
- Documentation

## Documentation

- **PROJECT_DOCUMENTATION.md**: Vision, problems, architecture, and why this matters
- **TECHNICAL_IMPLEMENTATION.md**: How to build and deploy each component
- **QUICK_REFERENCE.md**: Quick lookup for key concepts
- **APP_GUIDE.md**: How to use the application

Read in order:
1. QUICK_REFERENCE.md (5 min)
2. PROJECT_DOCUMENTATION.md (20 min)
3. TECHNICAL_IMPLEMENTATION.md (30 min)

## Team

- **Person 1**: Vault contract and token
- **Person 2**: Ticket system
- **Person 3**: Treasury pool (deployed)
- **Person 4**: Application frontend (home, savings, tickets screens)
- **Person 5**: Backend and integration (in progress)

## Current Numbers

- **Treasury Goal**: ₹100,000
- **Amount Raised**: ₹50,000 (50% complete)
- **Active Users**: Beta testing phase
- **Transactions**: On testnet only
- **Smart Contracts**: 1 live (treasury), 2 pending (vault, tickets)

## Roadmap

### Immediate (This Week)

- Deploy vault contract
- Implement ticket system
- Connect app to deployed contracts
- Public beta testing

### Short Term (Next 2 Weeks)

- Complete backend API
- Add mobile optimization
- Comprehensive testing
- Security audit

### Medium Term (1 Month)

- Production deployment
- University partnerships
- Mainnet migration
- Community launch

### Long Term

- Governance tokens
- Governance voting
- Insurance mechanisms
- Cross-campus integration

## License

MIT License. See [LICENSE.md](LICENSE.md)

## Contact

- GitHub Issues: Report bugs and request features
- Discussions: Ask questions and share ideas
- Email: [contact email]

## Deployment Links

### Live Demo (Testnet)

[Add deployed app URL once live]

### Blockchain Verification

- Treasury: https://testnet.algoexplorer.io/application/755379222
- Tokens: https://testnet.algoexplorer.io/asset/755379212

## Acknowledgments

Built during Hackspiration by students at KJSSE.

Powered by Algorand testnet and open source tools.

---

**Status**: 60% complete, open source, ready for contribution

**Latest Update**: Three screens built (home, savings, tickets)

**Next**: Connect frontend to deployed blockchain contracts
