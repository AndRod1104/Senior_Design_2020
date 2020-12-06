CREATE TABLE researcher (
	researcher_id serial,
	email varchar(50) not null,
	passwrd varchar(500) not null,
	f_name varchar(15) not null,
	m_initial char(1),
	l_name varchar(15) not null,
	institution varchar(50) not null,
	PRIMARY KEY (researcher_id),
	unique (email)
);

CREATE TABLE subject (
	subject_id serial,
	researcher_id serial,
	age integer not null,
	weight integer not null,
	height decimal(3,2) not null,
	bmi decimal(3,1) not null,
	ethnicity varchar(50) not null,
	fitzpatrick varchar(50) not null,
	gender varchar(20) not null,
	PRIMARY KEY (subject_id),
	FOREIGN KEY (researcher_id) REFERENCES researcher(researcher_id)
);

CREATE TABLE processed_data (
	body_location varchar(30) not null,
	subject_id serial,
	wave_length decimal(20,10) not null,
	absorbance decimal(20,10) not null,
	time_date timestamp not null,
	PRIMARY KEY (body_location, subject_id),
	FOREIGN KEY (subject_id) REFERENCES subject(subject_id)
);