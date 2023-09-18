import React from 'react';
import Navbar from '../../homepage/navbar/navbar';
import Footer from '../../homepage/footer/footer';
// redirection function
function ThankYouPage() {
  const handleRedirect = () => {
    window.location.href = '/';
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex flex-col items-center justify-center flex-1">
        <h1  className="text-center text-4xl font-bold mb-4">Thank you for taking the test,</h1>
        <h1  className="text-center text-4xl font-bold mb-4">you will receive the results soon.</h1>
        <button
          onClick={handleRedirect}
          className="mt-8 w-1/2 mx-auto bg-gradient-to-r from-a9e7ff via-1DCDFE to-a9e7ff hover:from-bbecff hover:via-31d2ff hover:to-bbecff hover:border-1DCDFE hover:text-white transition-colors duration-300 ease-in-out rounded-lg text-white font-bold text-3xl py-4"

        >
          Go to home page
        </button>
      </div>
      <Footer className="fixed bottom-0 left-0 right-0" />
    </div>
  );
}

export default ThankYouPage;