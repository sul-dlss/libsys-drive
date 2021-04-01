# frozen_string_literal: true

server 'symphony-app-prod-1.stanford.edu', user: fetch(:user).to_s, roles: %w[app db web]

# allow ssh to host
Capistrano::OneTimeKey.generate_one_time_key!
