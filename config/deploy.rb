# frozen_string_literal: true

set :application, 'libsys-drive'
set :repo_url, 'https://github.com/sul-dlss/libsys-drive.git'
set :user, 'sirsi'

# Default branch is :master
ask :branch, `git rev-parse --abbrev-ref HEAD`.chomp

# Default value for :log_level is :debug
set :log_level, :info

# Default deploy_to directory is /var/www/my_app_name
set :deploy_to, "/s/SUL/Bin/LibsysDrive/#{fetch(:application)}"

# Default value for linked_dirs is []
# set :linked_dirs, %w[]
set :linked_dirs, %w[cert]

# Default value for keep_releases is 5
set :keep_releases, 3

set :default_env, { path: '/s/sirsi/.rvm/gems/ruby-2.6.3/bin:/usr/local/rvm/gems/ruby-2.6.3/bin:'\
                          '/usr/local/rvm/gems/ruby-2.6.3@global/bin:/usr/local/rvm/rubies/ruby-2.6.3/bin:'\
                          '/usr/ucb:/bin:/usr/bin:/etc:/usr/sbin:/usr/local/rvm/bin' }

namespace :deploy do
  desc 'install dependencies'
  on roles(:app) do
    within release_path do
      execute 'source /s/SUL/Bin/py3-env/bin/activate && pip install -r requirements.txt'
    end
  end
end
