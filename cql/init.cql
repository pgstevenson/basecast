-- ENVIRONMENT --

DROP KEYSPACE IF EXISTS basecast;
CREATE KEYSPACE basecast WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };
USE basecast;

-- TABLES --

-- Users --

DROP TYPE IF EXISTS podcast_roles;

CREATE TYPE podcast_roles (
    podcast_id timeuuid,
    role int
);

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_email text,
	podcasts list<frozen<podcast_roles>>,
	PRIMARY KEY (user_email)
);

INSERT INTO users (user_email, podcasts) VALUES ('pstevenson6@gmail.com',
[{podcast_id: 98c8cd08-1a4a-11ef-a854-325096b39f47, role: 1},
{podcast_id:d74a045e-247a-11ef-b59b-325096b39f47, role:1}]);

-- Assets --

DROP TABLE IF EXISTS assets_by_podcasts;

CREATE TABLE assets_by_podcasts (
	podcast_id timeuuid,
	asset_id timeuuid,
	medallion text,
	type text,
	uri text,
	filename text,
	PRIMARY KEY (podcast_id, asset_id)
);

INSERT INTO assets_by_podcasts (podcast_id, asset_id, medallion, type, uri, filename) VALUES (98c8cd08-1a4a-11ef-a854-325096b39f47, 2e09e8b6-1a41-11ef-87d6-325096b39f47, 'gold', 'thumb', 'https://mcdn.podbean.com/mf/web/gtvdj9/logo3000x3000.png', 'logo3000x3000.png');
INSERT INTO assets_by_podcasts (podcast_id, asset_id, medallion, type, uri, filename) VALUES (98c8cd08-1a4a-11ef-a854-325096b39f47, 2e09ea96-1a41-11ef-b40e-325096b39f47, 'gold', 'thumb', 'https://mcdn.podbean.com/mf/web/dqkrm4nagkzv7dq7/Daniel_THUMB.jpg', 'Daniel_THUMB.jpg');
INSERT INTO assets_by_podcasts (podcast_id, asset_id, medallion, type, uri, filename) VALUES (98c8cd08-1a4a-11ef-a854-325096b39f47, 2e09eb04-1a41-11ef-ae03-325096b39f47, 'bronze', 'thumb', 'bronze/98c8cd08-1a4a-11ef-a854-325096b39f47/Daniel - Podcast.png', 'Daniel - Podcast.png');
INSERT INTO assets_by_podcasts (podcast_id, asset_id, medallion, type, uri, filename) VALUES (98c8cd08-1a4a-11ef-a854-325096b39f47, 2e09eb54-1a41-11ef-a3d3-325096b39f47, 'bronze', 'audio', 'bronze/98c8cd08-1a4a-11ef-a854-325096b39f47/Church intro.wav', 'Church intro.wav');
INSERT INTO assets_by_podcasts (podcast_id, asset_id, medallion, type, uri, filename) VALUES (98c8cd08-1a4a-11ef-a854-325096b39f47, 2e09eb9a-1a41-11ef-8ce7-325096b39f47, 'bronze', 'audio', 'bronze/98c8cd08-1a4a-11ef-a854-325096b39f47/Outro_Jul23.wav', 'Outro_Jul23.wav');

-- Episodes --

DROP TABLE IF EXISTS episodes_by_podcasts;

CREATE TABLE episodes_by_podcasts (
    episode_id timeuuid,
	podcast_id timeuuid,
	intro text,
	outro text,
    clips list<FROZEN<list<int>>>,
	title text,
	description text,
	status text,
	type text,
	logo text,
	filename text,
	PRIMARY KEY (podcast_id, episode_id)
);

-- Driver --

DROP TABLE IF EXISTS driver;

CREATE TABLE driver (
	job_id timeuuid,
	podcast_id timeuuid,
	episode_id timeuuid,
	filename text,
	PRIMARY KEY (job_id)
);

-- Podcasts --

DROP TABLE IF EXISTS podcasts;

CREATE TABLE podcasts (
    podcast_id timeuuid,
	client_id timeuuid,
	host_id text,
	host_secret text,
	title text,
	description text,
	logo text,
	intro text,
	outro text,
	blurb text,
	episode_logo text,
	PRIMARY KEY (podcast_id)
);

INSERT INTO podcasts (client_id, podcast_id, host_id, host_secret, title, description, logo, intro, outro, blurb, episode_logo) VALUES (
	98c8ca6a-1a4a-11ef-8519-325096b39f47,
	98c8cd08-1a4a-11ef-a854-325096b39f47,
	'a0de6fd07c0b8e0a09c23',
	'c117551131f73345640c7',
	'Blacktown Anglican Church',
	'Welcome to Blacktown Anglican Church! This podcast includes weekly sermons delivered by our ministry team. You can also watch the service live stream every Sunday at 10 AM AEST on YouTube at https://www.youtube.com/@BlacktownAnglican. Visit our website https://bac.org.au/ to find out more about our church, ministries, mission, and vision.',
	'https://mcdn.podbean.com/mf/web/gtvdj9/logo3000x3000.png',
	'bronze/98c8cd08-1a4a-11ef-a854-325096b39f47/Church intro.wav',
	'bronze/98c8cd08-1a4a-11ef-a854-325096b39f47/Outro_Jul23.wav',
	'<p>We live stream every Sunday at 10 AM (AEDT). Join us here:</p><p><a href="https://www.youtube.com/blacktownanglican">www.youtube.com/blacktownanglican</a></p><p>Or find us online at: <a href="https://bac.org.au/">bac.org.au</a></p>',
	'https://mcdn.podbean.com/mf/web/dqkrm4nagkzv7dq7/Daniel_THUMB.jpg'
);

INSERT INTO podcasts (client_id, podcast_id, host_id, host_secret, title) VALUES (
	d74a0238-247a-11ef-bc8b-325096b39f47,
	d74a045e-247a-11ef-b59b-325096b39f47,
	'482c8dc704220c415f566',
	'84b22d0f0114b8f6b23c5',
	'Sandbox'
);

-- Clients --

DROP TABLE IF EXISTS clients;

CREATE TABLE clients (
	client_id timeuuid,
	name text,
	tokens int,
	podcast_ids list<timeuuid>,
	PRIMARY KEY (client_id)
);

INSERT INTO clients (client_id, name, tokens, podcast_ids) VALUES (98c8ca6a-1a4a-11ef-8519-325096b39f47, 'Blacktown Anglican Church', 9999, [98c8cd08-1a4a-11ef-a854-325096b39f47]);
INSERT INTO clients (client_id, name, tokens, podcast_ids) VALUES (d74a0238-247a-11ef-bc8b-325096b39f47, 'pgstevenson.com', 9999, [d74a045e-247a-11ef-b59b-325096b39f47]);
