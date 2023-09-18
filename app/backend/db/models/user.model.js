const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const validator = require('validator');

const userSchema = new mongoose.Schema({
    email: {
        type: String,
        required: true,
        unique: true
    },
    password: {
        type: String,
        required: true
    },
    age: {
        type: Number,
        required: true
    },
    gender: {
        type: String,
        required: true
    },
    occupation: {
        type: String,
        required: true
    }
});

// static signup method
userSchema.statics.signup = async function(email, password, age, gender, occupation) {
    
    // validate email, password, age, gender and occupation
    if (!email || !password || !age || !gender || !occupation) {
        throw Error('All fields are required');
    }
    
    if (!validator.isEmail(email)) {
        throw Error('Email is not valid');
    }  

    if (!validator.isStrongPassword(password)) {
        throw Error('Password is not strong enough');
    }

    if (age <= 0) {
        throw Error('Age must be a positive number');
    }

    if (age < 18) {
        throw Error('Invalid age. You must be at least 18 years old to use this application.');
    }

    if (typeof occupation !== 'string' || occupation.length > 20) {
        throw Error('Occupation must be a string with maximum length of 20');
    }

    const exists = await this.findOne({ email });
    
    if (exists) {
        throw Error('Email already exists');
    }  

    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    const user = await this.create({ email, password: hashedPassword, age, gender, occupation });

    return user;
}


// static login method
userSchema.statics.login = async function(email, password) {
    if(!email || !password) {
        throw Error('Email and password are required');
    }

    const user = await this.findOne({ email });
    
    if (!user) {
        throw Error('Email or password is wrong');
    }

    const isMatch = await bcrypt.compare(password, user.password);

    if (!isMatch) {
        throw Error('Email or password is wrong');
    }

    return user;
}


module.exports = mongoose.model("User", userSchema)