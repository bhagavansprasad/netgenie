// import React from 'react';
// import './LoginPage.css';
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
// import { faEnvelope, faNetworkWired } from '@fortawesome/free-solid-svg-icons';
// import { faMicrosoft } from '@fortawesome/free-brands-svg-icons';


// function LoginPage() {
//   return (
//     <div id="login-page" className="min-h-screen bg-[#f3f3f3] flex items-center justify-center p-4">
//       <div className="w-full max-w-md">
//         {/* Logo Section */}
//         <div className="text-center mb-8">
//           <div className="flex items-center justify-center gap-2 text-2xl text-[#1a1a1a]">
//           <FontAwesomeIcon icon={faNetworkWired} className="text-3xl" />
//             NetGenie
//           </div>
//           <p className="text-[#5d5d5d] mt-2">Network Configuration Management</p>
//         </div>

//         {/* Login Form */}
//         <div className="bg-white rounded-lg shadow-lg p-8 backdrop-blur-xl bg-opacity-90">
//           <div className="space-y-6">
//             {/* Login Options */}
//             <div className="flex gap-4 mb-6">
//               <button className="flex-1 py-2.5 px-4 bg-[#fdfdfd] border border-[#e5e5e5] rounded-md flex items-center justify-center gap-2 hover:bg-[#f5f5f5] transition-colors">
//               <FontAwesomeIcon icon={faEnvelope} />
//                 Email
//               </button>
//               <button className="flex-1 py-2.5 px-4 bg-[#fdfdfd] border border-[#e5e5e5] rounded-md flex items-center justify-center gap-2 hover:bg-[#f5f5f5] transition-colors">
//               <FontAwesomeIcon icon={faMicrosoft} />
//                 SSO
//               </button>
//             </div>

//             <div className="relative">
//               <div className="absolute inset-0 flex items-center">
//                 <div className="w-full border-t border-[#e5e5e5]"></div>
//               </div>
//               <div className="relative flex justify-center text-sm">
//                 <span className="px-2 bg-white text-[#5d5d5d]">or continue with email</span>
//               </div>
//             </div>

//             {/* Email Input */}
//             <div>
//               <label className="block text-sm text-[#1a1a1a] mb-1">Email</label>
//               <input
//                 type="email"
//                 className="w-full px-3 py-2 bg-[#fdfdfd] border border-[#e5e5e5] rounded-md focus:ring-2 focus:ring-[#0067c0] focus:border-[#0067c0] transition-colors"
//                 placeholder="name@company.com"
//               />
//             </div>

//             {/* Password Input */}
//             <div>
//               <label className="block text-sm text-[#1a1a1a] mb-1">Password</label>
//               <input
//                 type="password"
//                 className="w-full px-3 py-2 bg-[#fdfdfd] border border-[#e5e5e5] rounded-md focus:ring-2 focus:ring-[#0067c0] focus:border-[#0067c0] transition-colors"
//                 placeholder="••••••••"
//               />
//             </div>

//             {/* Remember & Forgot */}
//             <div className="flex items-center justify-between">
//               <div className="flex items-center">
//                 <input type="checkbox" className="h-4 w-4 border-[#e5e5e5] rounded accent-[#0067c0]" />
//                 <label className="ml-2 text-sm text-[#5d5d5d]">Remember me</label>
//               </div>
//               <button className="text-sm text-[#0067c0] hover:text-[#005aa7] transition-colors">Forgot password?</button>
//             </div>

//             {/* Login Button */}
//             <button className="w-full bg-[#0067c0] text-white py-2.5 rounded-md hover:bg-[#005aa7] transition-colors">
//               Sign in
//             </button>
//           </div>
//         </div>

//         {/* Admin Registration */}
//         <div className="mt-6 text-center">
//           <span className="text-sm text-[#5d5d5d]">Need an account? </span>
//           <button className="text-sm text-[#0067c0] hover:text-[#005aa7] hover:underline transition-colors">Contact Admin</button>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default LoginPage;




import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faNetworkWired,
  faEnvelope,
} from '@fortawesome/free-solid-svg-icons';
import { faMicrosoft } from '@fortawesome/free-brands-svg-icons';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
  const navigate = useNavigate(); // Get the navigate function

  const handleLogin = () => {
    // Simulate a successful login
    // In a real application, you would authenticate with a server
    console.log('Login successful!');
    navigate('/dashboard'); // Redirect to dashboard after login
  };

  return (
    <div className="min-h-screen bg-[#f3f3f3] flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo Section */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 text-2xl text-[#1a1a1a]">
            <FontAwesomeIcon icon={faNetworkWired} className="text-3xl" />
            NetGenie
          </div>
          <p className="text-[#5d5d5d] mt-2">
            Network Configuration Management
          </p>
        </div>

        {/* Login Form */}
        <div className="bg-white rounded-lg shadow-lg p-8 backdrop-blur-xl bg-opacity-90">
          <div className="space-y-6">
            {/* Login Options */}
            <div className="flex gap-4 mb-6">
              <button className="flex-1 py-2.5 px-4 bg-[#fdfdfd] border border-[#e5e5e5] rounded-md flex items-center justify-center gap-2 hover:bg-[#f5f5f5] transition-colors">
                <FontAwesomeIcon icon={faEnvelope} />
                Email
              </button>
              <button className="flex-1 py-2.5 px-4 bg-[#fdfdfd] border border-[#e5e5e5] rounded-md flex items-center justify-center gap-2 hover:bg-[#f5f5f5] transition-colors">
                <FontAwesomeIcon icon={faMicrosoft} />
                SSO
              </button>
            </div>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-[#e5e5e5]"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-[#5d5d5d]">
                  or continue with email
                </span>
              </div>
            </div>

            {/* Email Input */}
            <div>
              <label className="block text-sm text-[#1a1a1a] mb-1">
                Email
              </label>
              <input
                type="email"
                className="w-full px-3 py-2 bg-[#fdfdfd] border border-[#e5e5e5] rounded-md focus:ring-2 focus:ring-[#0067c0] focus:border-[#0067c0] transition-colors"
                placeholder="name@company.com"
              />
            </div>

            {/* Password Input */}
            <div>
              <label className="block text-sm text-[#1a1a1a] mb-1">
                Password
              </label>
              <input
                type="password"
                className="w-full px-3 py-2 bg-[#fdfdfd] border border-[#e5e5e5] rounded-md focus:ring-2 focus:ring-[#0067c0] focus:border-[#0067c0] transition-colors"
                placeholder="••••••••"
              />
            </div>

            {/* Remember & Forgot */}
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  className="h-4 w-4 border-[#e5e5e5] rounded accent-[#0067c0]"
                />
                <label className="ml-2 text-sm text-[#5d5d5d]">
                  Remember me
                </label>
              </div>
              <button className="text-sm text-[#0067c0] hover:text-[#005aa7] transition-colors">
                Forgot password?
              </button>
            </div>

            {/* Login Button */}
            <button className="w-full bg-[#0067c0] text-white py-2.5 rounded-md hover:bg-[#005aa7] transition-colors"  onClick={handleLogin}>
              Sign in
            </button>
          </div>
        </div>

        {/* Admin Registration */}
        <div className="mt-6 text-center">
          <span className="text-sm text-[#5d5d5d]">
            Need an account?{' '}
          </span>
          <button className="text-sm text-[#0067c0] hover:text-[#005aa7] hover:underline transition-colors">
            Contact Admin
          </button>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
