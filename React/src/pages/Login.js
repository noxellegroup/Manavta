import React from 'react'

export default function Login() {
  return (
    <React.Fragment>
        <div class="container" id="container">
	
	<div class="form-container sign-in-container">
		<form action="#">
			<h1 style="color: white;">Sign in</h1>
			<div class="social-container">
				<a href="#" class="social"><i class="fab fa-facebook-f"></i></a>
				<a href="#" class="social"><i class="fab fa-google-plus-g"></i></a>
				<a href="#" class="social"><i class="fab fa-linkedin-in"></i></a>
			</div>
			<span style="color: white;">or use your account</span>
			<input type="email" placeholder="Email"/>
			<input type="password" placeholder="Password" />
			<a href="#">Forgot your password?</a>
			<button>Sign In</button>
		</form>
	</div>
	<div class="overlay-container">
		<div class="overlay">
			
			<div class="overlay-panel overlay-right">
				<h1>Product Description</h1>
			</div>
		</div>
	</div>
</div>

    </React.Fragment>
  )
}
