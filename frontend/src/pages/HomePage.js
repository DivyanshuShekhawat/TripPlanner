import React from 'react';
import { Box, Typography, Button, Container, Grid, Card, CardMedia, CardContent, CardActions } from '@mui/material';
import { styled } from '@mui/material/styles';
import { useNavigate } from 'react-router-dom';

const HeroSection = styled(Box)(({ theme }) => ({
  position: 'relative',
  height: '70vh',
  display: 'flex',
  alignItems: 'center',
  color: theme.palette.common.white,
  backgroundImage: 'linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url(https://source.unsplash.com/random/1600x900/?travel)',
  backgroundSize: 'cover',
  backgroundPosition: 'center',
}));

const FeatureCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  transition: 'transform 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-5px)',
    boxShadow: theme.shadows[10],
  },
}));

const destinations = [
  {
    id: 1,
    name: 'Paris',
    image: 'https://source.unsplash.com/random/300x200/?paris',
    description: 'Discover the romance and beauty of the City of Lights.',
  },
  {
    id: 2,
    name: 'Bali',
    image: 'https://source.unsplash.com/random/300x200/?bali',
    description: 'Experience tropical paradise with stunning beaches and rich culture.',
  },
  {
    id: 3,
    name: 'Tokyo',
    image: 'https://source.unsplash.com/random/300x200/?tokyo',
    description: 'Explore the perfect blend of tradition and cutting-edge technology.',
  },
];

const features = [
  {
    title: 'Personalized Recommendations',
    description: 'Get destination recommendations tailored to your preferences and travel history.',
    image: 'https://source.unsplash.com/random/300x200/?map',
  },
  {
    title: 'Smart Budget Planning',
    description: 'Plan your trip with accurate price predictions and budget optimization.',
    image: 'https://source.unsplash.com/random/300x200/?money',
  },
  {
    title: 'AI-Powered Itineraries',
    description: 'Generate optimized itineraries based on your interests and time constraints.',
    image: 'https://source.unsplash.com/random/300x200/?schedule',
  },
];

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <Box>
      <HeroSection>
        <Container maxWidth="md">
          <Typography variant="h2" component="h1" gutterBottom>
            Plan Your Perfect Trip
          </Typography>
          <Typography variant="h5" paragraph>
            Discover personalized travel recommendations and itineraries powered by AI
          </Typography>
          <Box mt={4}>
            <Button 
              variant="contained" 
              color="primary" 
              size="large"
              onClick={() => navigate('/planner')}
            >
              Start Planning
            </Button>
            <Button 
              variant="outlined" 
              color="inherit" 
              size="large" 
              sx={{ ml: 2 }}
              onClick={() => navigate('/explore')}
            >
              Explore Destinations
            </Button>
          </Box>
        </Container>
      </HeroSection>

      <Container maxWidth="lg" sx={{ mt: 8, mb: 8 }}>
        <Typography variant="h3" component="h2" align="center" gutterBottom>
          How It Works
        </Typography>
        <Typography variant="h6" align="center" color="textSecondary" paragraph>
          Our AI-powered platform helps you create the perfect trip with just a few clicks
        </Typography>
        
        <Grid container spacing={4} mt={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={4} key={index}>
              <FeatureCard>
                <CardMedia
                  component="img"
                  height="200"
                  image={feature.image}
                  alt={feature.title}
                />
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography gutterBottom variant="h5" component="h2">
                    {feature.title}
                  </Typography>
                  <Typography>
                    {feature.description}
                  </Typography>
                </CardContent>
              </FeatureCard>
            </Grid>
          ))}
        </Grid>
      </Container>

      <Box sx={{ bgcolor: 'background.paper', py: 8 }}>
        <Container maxWidth="lg">
          <Typography variant="h3" component="h2" align="center" gutterBottom>
            Popular Destinations
          </Typography>
          <Typography variant="h6" align="center" color="textSecondary" paragraph>
            Explore some of our users' favorite places
          </Typography>
          
          <Grid container spacing={4} mt={4}>
            {destinations.map((destination) => (
              <Grid item key={destination.id} xs={12} sm={6} md={4}>
                <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                  <CardMedia
                    component="img"
                    height="200"
                    image={destination.image}
                    alt={destination.name}
                  />
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Typography gutterBottom variant="h5" component="h2">
                      {destination.name}
                    </Typography>
                    <Typography>
                      {destination.description}
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button size="small" onClick={() => navigate(`/explore?destination=${destination.name}`)}>
                      Learn More
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      <Container maxWidth="lg" sx={{ mt: 8, mb: 8, textAlign: 'center' }}>
        <Typography variant="h3" component="h2" gutterBottom>
          Ready to Plan Your Next Adventure?
        </Typography>
        <Typography variant="h6" color="textSecondary" paragraph>
          Create your personalized trip plan in minutes
        </Typography>
        <Button 
          variant="contained" 
          color="primary" 
          size="large"
          onClick={() => navigate('/register')}
        >
          Get Started
        </Button>
      </Container>
    </Box>
  );
};

export default HomePage; 